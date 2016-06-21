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

-module(kolab_guam_listener).

-behaviour(supervisor).
-define(DEFAULT_IMAP_PORT, 143).

%% API
-export([start_link/2, create_initial_listeners/1, cleanup/1]).

%% gen_supervisor callbacks
-export([init/1]).

%% state record definition
%%TODO: support reconfiguration requests

%% public API
start_link(Name, Config) -> supervisor:start_link(?MODULE, [Name, Config]).

%% gen_server API
init([Name, Config]) ->
    Host = proplists:get_value(host, Config, none),
    Port = proplists:get_value(port, Config, ?DEFAULT_IMAP_PORT),
    ImplicitTLS = proplists:get_value(implicit_tls, Config, false),
    TLSConfig = proplists:get_value(tls_config, Config, []),
    Rules = proplists:get_value(rules, Config, []),
    Options = listen_options(Host, ImplicitTLS, TLSConfig),
    lager:info("Starting listener \"~p\" on port ~B (~p) with ~B rules", [Name, Port, Options, length(Rules)]),
    { ok, ListenSocket } = listen(ImplicitTLS, Port, Options),
    spawn_link(?MODULE, cleanup, [ListenSocket]),
    %% setting up the initial listeners must be done async to allow the init to be done and the supervisor to be setup
    spawn_link(kolab_guam_listener, create_initial_listeners, [self()]),
    ImapConfig = imap_config(proplists:get_value(imap_server, Config, none)),
    lager:debug("ImapConfig is ~p", [ImapConfig]),
    {ok, { { simple_one_for_one, 60, 3600 },
         [ { session, { kolab_guam_session, start_link, [self(), ListenSocket, ImapConfig, ImplicitTLS, TLSConfig, Rules] }, temporary, 1000, worker, [kolab_guam_session] } ]
         }
    }.

imap_config(none) -> kolab_guam_sup:default_imap_server_config();
imap_config(Backend) -> kolab_guam_sup:imap_server_config(Backend).

listen_options(none, ImplicitTLS, TLSConfig) -> default_listen_options(ImplicitTLS, TLSConfig);
listen_options(Hostname, ImplicitTLS, TLSConfig) ->
    case inet:gethostbyname(Hostname) of
        { ok, { hostent, _HostName, _Unused, inet, _Ver, [IP] } } ->
            [ { ip, IP } | default_listen_options(ImplicitTLS, TLSConfig) ];
        _ ->
            listen_options(none, ImplicitTLS, TLSConfig)
    end.

default_listen_options(true, TLSConfig) -> [ { reuseaddr, true }, {active, once } | TLSConfig ];
default_listen_options(_ImplicitTLS, _Config) ->  [ { active, once }, { reuseaddr, true } ].

create_initial_listeners(PID) when is_pid(PID) ->
    lager:debug("Creating session pool for listener ~p", [PID]),
    [ supervisor:start_child(PID, []) || _ <- lists:seq(1, 20) ].

cleanup(Socket) ->
    process_flag(trap_exit, true),
    receive
        { 'EXIT', _PID, _  } -> ok;
        _ -> cleanup(Socket)
    end,
    gen_tcp:close(Socket).

listen(true, Port, Options) -> ssl:listen(Port, Options);
listen(_ImplicitTLS, Port, Options) -> gen_tcp:listen(Port, Options).

%% private API

