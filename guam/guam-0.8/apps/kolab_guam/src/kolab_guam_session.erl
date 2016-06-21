%% Copyright 2015 Kolab Systems AG (http://www.kolabsys.com)
%%
%% Aaron Seigo (Kolab Systems) <seigo a kolabsys.com>
%%
%% This program is free software: you can redistribute it and/or modify
%% it under the terms of the GNU General Public License as published by
%% the Free Software Foundation, either version 3 of the License, or
%% (at your option) any later version.
%%
%% This program is distributed in the hope that it will be useful,
%% but WITHOUT ANY WARRANTY; without even the implied warranty of
%% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
%% GNU General Public License for more details.
%%
%% You should have received a copy of the GNU General Public License
%% along with this program.  If not, see <http://www.gnu.org/licenses/>.

-module(kolab_guam_session).

-behaviour(gen_server).

%% API
-export([ start_link/6 ]).

%% gen_server callbacks
-export([init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2, code_change/3]).

%% state record definition
-record(state, { socket, super_pid, tls_config = [], client_implicit_tls = false, client_tls_active = false, server_config = [],
                 rules_active = [], rules_deciding = [], imap_session, inflator, deflator }).

%% public API
start_link(SupervisorPID, ListenSocket, ImapConfig, ImplicitTLS, TLSConfig, Rules) -> gen_server:start_link(?MODULE, [SupervisorPID, ListenSocket, ImapConfig, ImplicitTLS, TLSConfig, Rules], []).

%% gen_server API
init([SupervisorPID, ListenSocket, ServerConfig, ImplicitTLS, TLSConfig, Rules]) ->
    %% accepting a connection is blocking .. so do it async
    %% lager:debug("Starting a session handler on socket ~p for listener ~p", [ListenSocket, SupervisorPID]),
    process_flag(trap_exit, true),
    ActiveRules = init_rules(Rules),
    gen_server:cast(self(), accept),
    %% lager:debug("Rules are ~p from ~p", [ActiveRules, Rules]),
    { ok, #state{ socket = ListenSocket, super_pid = SupervisorPID, client_implicit_tls = ImplicitTLS, tls_config = TLSConfig, server_config = ServerConfig, rules_deciding = ActiveRules } }.

handle_call(_Request, _From, State) ->
    { reply, ok, State }.

handle_cast(accept, State = #state{ socket = ListenSocket, server_config = ServerConfig }) ->
    { ok, AcceptSocket, TLSActive } = accept_client(ListenSocket, State),
    { ok, ImapSession } = eimap:start_link(ServerConfig),
    eimap:connect(ImapSession, self(), server_hello),
    { noreply, State#state{ socket = AcceptSocket, imap_session = ImapSession, client_tls_active = TLSActive } };
handle_cast(_Msg, State) ->
    { noreply, State }.

handle_info({ tcp_closed, _Socket }, State) ->
    %lager:debug("Client closed socket"),
    { stop, normal, State };
handle_info({ tcp_error, _Socket, _Error }, State) ->
    %lager:debug("Socket error"),
    { stop, normal, State };
handle_info({ ssl_closed, _Socket }, State) ->
    %lager:debug("Client closed socket"),
    { stop, normal, State };
handle_info({ ssl_error, _Socket, _Error }, State) ->
    %lager:debug("Socket error"),
    { stop, normal, State };
handle_info({ tcp, Socket, Data }, #state{ client_tls_active = false } = State) ->
    %lager:debug("Data coming in from client over TCP ~s", [Data]),
    process_client_data(Socket, Data, State);
handle_info({ ssl, Socket, Data }, State) ->
    %lager:debug("Data coming in from client over SSL, ~p", [Data]),
    process_client_data(Socket, Data, State);
handle_info({ server_hello, ServerHello }, #state{ imap_session = ImapSession, tls_config = TLSConfig, socket = Socket, client_tls_active = TLSActive, deflator = Deflator } = State) ->
    CorrectedHello = correct_hello(TLSActive, TLSConfig, ServerHello),
    eimap:start_passthrough(ImapSession, self()),
    relay_response(Socket, postprocess_server_data(Deflator, <<CorrectedHello/binary, "\r\n">>), TLSActive),
    { noreply, State };
handle_info({ { rule_data, Module, ResponseToken }, Data }, #state{ rules_active = ActiveRules } = State) ->
    %lager:debug("Got back data requested by rule ~p: ~p", [Module, Data]),
    NewActiveRules =
    case proplists:get_value(Module, ActiveRules) of
        undefined -> ActiveRules;
        ModuleState ->
            NewModuleState = Module:imap_data(ResponseToken, Data, ModuleState),
            lists:reverse(lists:foldl(fun({ Rule, RuleState }, Acc) ->
                                              case Rule =:= Module of
                                                  true -> [{ Rule, NewModuleState }|Acc];
                                                  _ -> [{ Rule, RuleState }|Acc]
                                              end
                                      end,
                          [], ActiveRules))
    end,
    %TODO: should we also support non-active rules doing imapy things here?
    { noreply, State#state{ rules_active = NewActiveRules } };
handle_info({ imap_server_response, Data }, #state{ socket = Socket, imap_session = ImapSession, client_tls_active = TLS, deflator = Deflator, rules_active = ActiveRules } = State) ->
    %lager:debug("FROM SERVER: ~s", [Data]),
    { ModifiedData, CurrentlyActiveRules } = apply_ruleset_serverside(ImapSession, Data, ActiveRules),
    relay_response(Socket, postprocess_server_data(Deflator, ModifiedData), TLS),
    { noreply, State#state{ rules_active = CurrentlyActiveRules } };
handle_info({ 'EXIT', PID, _Reason }, #state { imap_session = PID } = State) ->
    { stop, normal, State };
handle_info(Info, State) ->
    lager:debug("Received unexpected info... ~p", [Info]),
    { noreply, State }.

terminate(_Reason, #state{ inflator = Inflator, deflator = Deflator, socket = Socket, client_tls_active = TLS }) ->
    %lager:debug("Termination!~p", [self()]),
    close_zlib_handle(Inflator),
    close_zlib_handle(Deflator),
    close_socket(TLS, Socket),
    ok.

code_change(_OldVsn, State, _Extra) ->
    { ok, State }.

%% private API
accept_client(ListenSocket, #state{ client_implicit_tls = true, super_pid = SupervisorPID }) ->
    { ok, AcceptSocket } = ssl:transport_accept(ListenSocket),
    ok = ssl:ssl_accept(AcceptSocket),
    ok = ssl:setopts(AcceptSocket, [{ active, once }, { mode, binary }]),
    %% start a new accepting process to replace this one, which is now i use
    supervisor:start_child(SupervisorPID, []),
    ok = ssl:setopts(ListenSocket, [{ active, once }, { mode, binary }]),
    % lager:info("~p All done!", [self()]),
    { ok, AcceptSocket, true };
accept_client(ListenSocket, #state{ super_pid = SupervisorPID }) ->
    { ok, AcceptSocket } = gen_tcp:accept(ListenSocket),
    ok = inet:setopts(AcceptSocket, [{ active, once }, { mode, binary }]),
    %% start a new accepting process to replace this one, which is now i use
    supervisor:start_child(SupervisorPID, []),
    ok = inet:setopts(ListenSocket, [{ active, once }]),
    { ok, AcceptSocket, false }.

close_zlib_handle(undefined) -> ok;
close_zlib_handle(Z) -> zlib:close(Z).

close_socket(_TLS, undefined) -> ok;
close_socket(true, Socket) -> ssl:close(Socket);
close_socket(_TLS, Socket) -> gen_tcp:close(Socket).

process_client_data(Socket, Data, #state{ rules_deciding = UndecidedRules, tls_config = TLSConfig, client_tls_active = TLS, rules_active = ActiveRules, socket = Socket, imap_session = ImapSession, inflator = Inflator, deflator = Deflator, server_config = ServerConfig } = State) ->
    %%TODO: multipacket input from clients
    % TODO: refactor so starttls and compress commands can be made into rules
    PreprocessData = preprocess_client_data(Inflator, Data),
    %lager:info("FROM CLIENT: ~s", [PreprocessData]),
    { TLSActive, CurrentSocket, CurrentInflator, CurrentDeflator, CurrentUndecidedRules, CurrentActiveRules } =
    case check_for_transmission_change_commands(TLS, TLSConfig, PreprocessData, Deflator, Socket) of
        { socket_upgraded, SSLSocket } ->
            %% if we have upgraded our socket, then do so to the backend if that hasn't happened auomatically
            case proplists:get_value(implicit_tls, ServerConfig, false) of
                false -> eimap:starttls(ImapSession, undefined, undefined);
                _ -> ok
            end,
            { true, SSLSocket, Inflator, Deflator, UndecidedRules, ActiveRules };
        { compression, NewInflator, NewDeflator } ->
            eimap:compress(ImapSession), % TODO: make optional
            { TLS, Socket, NewInflator, NewDeflator, UndecidedRules, ActiveRules };
        nochange ->
            %%lager:debug("... now applying rules"),
            { ModifiedData, NewUndecidedRules, NewActiveRules } = apply_ruleset_clientside(ImapSession, Socket, PreprocessData, UndecidedRules, ActiveRules),
            %%lager:info("The modified data is: ~s", [ModifiedData]),
            %lager:info("The post-processed data is: ~s", [PostProcessed]),
            eimap:passthrough_data(ImapSession, ModifiedData),
            { TLS, Socket, Inflator, Deflator, NewUndecidedRules, NewActiveRules}
    end,
    set_socket_active(TLSActive, CurrentSocket),
    { noreply, State#state{ rules_deciding = CurrentUndecidedRules, rules_active = CurrentActiveRules,
                            socket = CurrentSocket, client_tls_active = TLSActive,
                            inflator = CurrentInflator, deflator = CurrentDeflator } }.

preprocess_client_data(undefined, Data) ->
    Data;
preprocess_client_data(Z, Data) ->
    joined(zlib:inflate(Z, Data), <<>>).

postprocess_server_data(undefined, Data) ->
    %% we aren't compressing so there is nothing to do
    Data;
postprocess_server_data(Z, Data) ->
    joined(zlib:deflate(Z, Data, sync), <<>>).

joined([], Binary) -> Binary;
joined([H|Rest], Binary) -> joined(Rest, <<Binary/binary, H/binary>>).

init_rules(RuleConfig) -> init_rule(RuleConfig, []).
init_rule([], Acc) -> Acc;
init_rule([{ RuleName, Config }|RuleConfig], Acc) ->
    Module = full_rule_name(RuleName),
    %% we try to new the module, but if something goes wrong, e.g. it does not exist,
    %% then we skip this config block because it is BROKEN
    try Module:new(Config) of
        ModuleState -> init_rule(RuleConfig, [{ Module, ModuleState }|Acc])
    catch
        Type:Error ->
            lager:warning("Could not create rule for ~p due to failure: ~p ~p", [RuleName, Type, Error]),
            init_rule(RuleConfig, Acc)
    end;
init_rule([_|RuleConfig], Acc) ->
    init_rule(RuleConfig, Acc).

full_rule_name(Module) when is_atom(Module) -> list_to_atom("kolab_guam_rule_" ++ atom_to_list(Module)).

apply_ruleset_serverside(ImapSession, ServerData, CurrentlyActiveRules) ->
    %TODO: allow undecided rules to opt-in here as well
    apply_next_rule_serverside(ImapSession, ServerData, [], CurrentlyActiveRules).

apply_next_rule_serverside(_ImapSession, ServerData, ActiveRulesAcc, []) -> { ServerData, lists:reverse(ActiveRulesAcc) };
apply_next_rule_serverside(ImapSession, ServerData, ActiveRulesAcc, [{ Module, RuleState } | ActiveRules]) ->
    %TODO: allow rules to remove themselves from the action during serverside processing?
    { ModifiedData, ModifiedRuleState } = Module:apply_to_server_message(ImapSession, ServerData, RuleState),
    apply_next_rule_serverside(ImapSession, ModifiedData, [{ Module, ModifiedRuleState } | ActiveRulesAcc], ActiveRules).

apply_ruleset_clientside(ImapSession, Socket, ClientData, UndecidedRules, CurrentlyActiveRules) ->
    { StillUndecided, NewlyActive } = check_undecided(Socket, ClientData, UndecidedRules),
    ActiveRules = CurrentlyActiveRules ++ NewlyActive,
    { ModifiedData, ActiveRulesRun } = apply_next_rule_clientside(ImapSession, ClientData, [], ActiveRules),
    { ModifiedData, StillUndecided, ActiveRulesRun }.

check_undecided(Socket, ClientData, Rules) -> check_next_undecided_rule(Socket, ClientData, Rules, { [], [] }).
check_next_undecided_rule(_Socket, _ClientData, [], Accs) -> Accs;
check_next_undecided_rule(Socket, ClientData, [Rule|Rules], { UndecidedAcc, NewActiveAcc }) ->
    { Module, RuleState } = Rule,
    %%lager:debug("Does ~p apply with state ~p? let's find out!", [Module, RuleState]),
    check_next_undecided_rule(Socket, ClientData, Rules, applies(Module, Module:applies(Socket, ClientData, RuleState), UndecidedAcc, NewActiveAcc)).

applies(Module, { true, RuleState }, UndecidedAcc, NewActiveAcc) -> { UndecidedAcc, [{ Module, RuleState }|NewActiveAcc] };
applies(_Module, { false, _RuleState }, UndecidedAcc, NewActiveAcc) -> { UndecidedAcc, NewActiveAcc };
applies(Module, { notyet, RuleState }, UndecidedAcc, NewActiveAcc) -> { [{ Module, RuleState }|UndecidedAcc], NewActiveAcc }.

apply_next_rule_clientside(_ImapSession, ClientData, ActiveRulesAcc, []) -> { ClientData, lists:reverse(ActiveRulesAcc) };
apply_next_rule_clientside(ImapSession, ClientData, ActiveRulesAcc, [{ Module, RuleState }|Rules]) ->
    { Data, NewState } = Module:apply_to_client_message(ImapSession, ClientData, RuleState),
    apply_next_rule_clientside(ImapSession, Data, [{ Module, NewState } | ActiveRulesAcc], Rules).

relay_response(Socket, Data, false) ->
    %lager:debug("Sending over non-secure socket ..."),
    gen_tcp:send(Socket, Data);
relay_response(Socket, Data, _TLS) ->
    %lager:debug("Sending over TLS!"),
    ssl:send(Socket, Data).

check_for_transmission_change_commands(TLS, TLSConfig, Buffer, Deflator, Socket) ->
    {Tag, Command, _Data } = eimap_utils:split_command_into_components(Buffer),
    case check_tls_state(TLS, TLSConfig, Command, Deflator, Socket, Tag) of
        nochange -> check_compress_request(Deflator, Command, Socket, TLS, Tag);
        Response -> Response
    end.

check_tls_state(false, TLSConfig, <<"STARTTLS">>, Deflator, Socket, Tag) -> start_client_tls(TLSConfig, Deflator, Socket, Tag);
check_tls_state(false, TLSConfig, <<"starttls">>, Deflator, Socket, Tag) -> start_client_tls(TLSConfig, Deflator, Socket, Tag);
check_tls_state(_TLS, _TLSConfig, _Buffer, _Deflator, _Socket, _Tag) -> nochange.

start_client_tls(TLSConfig, Deflator, Socket, Tag) ->
    Response = <<Tag/binary, " OK Begin TLS negotiation now\r\n">>,
    relay_response(Socket, postprocess_server_data(Deflator, Response), false),
    { ok, SSLSocket } = ssl:ssl_accept(Socket, TLSConfig),
    { socket_upgraded, SSLSocket }.

check_compress_request(undefined, <<"COMPRESS">>, Socket, TLS, Tag) -> start_client_compression(Socket, TLS, Tag);
check_compress_request(undefined, <<"compress">>, Socket, TLS, Tag) -> start_client_compression(Socket, TLS, Tag);
check_compress_request(_Deflator, _Command, _Socket, _TLS, _Tag) -> nochange.

start_client_compression(Socket, TLS, Tag) ->
    Response = <<Tag/binary, " OK DEFLATE active\r\n">>,
    relay_response(Socket, postprocess_server_data(undefined, Response), TLS),
    %% create an inflate/deflate pair for use with the client
    Inflator = zlib:open(),
    ok = zlib:inflateInit(Inflator, -15),
    Deflator = zlib:open(),
    ok = zlib:deflateInit(Deflator, 1, deflated, -15, 8, default),
    { compression, Inflator, Deflator }.


set_socket_active(true, Socket) -> ssl:setopts(Socket, [{ active, once }]);
set_socket_active(_, Socket) -> inet:setopts(Socket, [{ active, once }]).

-spec correct_hello(TLSActive :: true | false, TlSConfig :: [] | list(), ServerHello :: binary()) -> CorrectedHello :: binary().
correct_hello(true, _TLSConfig, ServerHello) ->
    % the connection is already secured, so don't advertise starttls to the client
    ensure_hello_does_not_have_starttls(ServerHello);
correct_hello(_TLSActive, [], ServerHello) ->
    % guam does not have a TLS config and so can not provide TLS to the client
    ensure_hello_does_not_have_starttls(ServerHello);
correct_hello(_TLSAcive, _TLSConfig, ServerHello) ->
    % guam has a TLS config, and it is not currently active, so make sure to include
    % STARTTLS in our response regardless of what the backend says
    ensure_hello_has_starttls(ServerHello).

ensure_hello_has_starttls(ServerResponse) ->
    ServerHello = proplists:get_value(capabilities, ServerResponse, <<>>),
    case binary:match(ServerHello, <<"STARTTLS">>) of
        nomatch -> add_starttls_to_capabilities(ServerHello);
        _ -> ServerHello
    end.

add_starttls_to_capabilities(ServerHello) ->
    case binary:match(ServerHello, <<"CAPABILITY ">>) of
        nomatch -> ServerHello;
        { Start, End } ->
            Prefix = binary:part(ServerHello, 0, Start + End),
            Suffix = binary:part(ServerHello, Start + End, size(ServerHello) - Start - End),
            <<Prefix/binary, "STARTTLS ", Suffix/binary>>
    end.

ensure_hello_does_not_have_starttls(ServerHello) ->
    case binary:match(ServerHello, <<"STARTTLS">>) of
        nomatch -> ServerHello;
        { Start, End } ->
            Prefix = binary:part(ServerHello, 0, Start),
            Suffix = binary:part(ServerHello, Start + End, size(ServerHello) - Start - End),
            <<Prefix/binary, Suffix/binary>>
    end.

