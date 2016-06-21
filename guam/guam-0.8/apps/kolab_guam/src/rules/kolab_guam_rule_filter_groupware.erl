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

-module(kolab_guam_rule_filter_groupware).
-export([new/1, applies/3, imap_data/3, apply_to_client_message/3, apply_to_server_message/3]).
-behavior(kolab_guam_rule).

-record(state, { blacklist = [], tag = <<>>, active = false, last_chunk = <<>>,
                 trigger_commands = [<<"LIST">>, <<"list">>, <<"XLIST">>, <<"xlist">>, <<"LSUB">>, <<"lsub">>]}).

new(_Config) -> #state { blacklist = undefined }.

applies(_ConnectionDetails, Buffer, State) ->
    { _Tag, Command, Data } = eimap_utils:split_command_into_components(Buffer),
    %lager:debug("********** Checking ...~n    Command: ~s ~s", [Command, Data]),
    { apply_if_id_matches(Command, Data, State#state.trigger_commands), State }.

apply_to_client_message(ImapSession, Buffer, State) ->
    { Tag, Command, Data } = eimap_utils:split_command_into_components(Buffer),
    { Active, StateTag }=
    case lists:any(fun(T) -> (Command =:= T) andalso
                             ((binary:match(Data, <<"*">>) =/= nomatch) orelse (binary:match(Data, <<"%">>) =/= nomatch)) end,
                   State#state.trigger_commands) of
        true -> fetch_metadata(ImapSession, State), { true, Tag };
        _ -> { false, <<>> }
    end,
    %lager:info("Client sent: ~s ~s ~p", [Command, Data, Active]),
    { Buffer, State#state{ active = Active, tag = StateTag }}.

apply_to_server_message(_ImapSession, Buffer, #state{ active = true } = State) ->
    filter_folders(Buffer, State);
apply_to_server_message(_ImapSession, Buffer, State) -> { Buffer, State }.

imap_data(blacklist, { error, _Reason }, State) -> State;
imap_data(blacklist, Response, State) ->
    %TODO: we don't need Foo/Bar if we already have Foo, so filter folders-of-groupwarefolders
    Blacklist = lists:foldl(fun({ _Folder, [ { _Property, null } ]}, Acc) -> Acc;
                               ({ _Folder, [ { _Property, <<"mail", _Rest/binary>> } ]}, Acc) -> Acc;
                               ({ Folder, _ }, Acc) -> [{ Folder, <<Folder/binary, "/">> }|Acc] end,
                            [], Response),
    State#state{ blacklist = Blacklist }.

%%PRIVATE

fetch_metadata(none, #state{ blacklist = undefined }) -> ok;
fetch_metadata(ImapSession, #state{ blacklist = undefined }) ->
    eimap:get_folder_metadata(ImapSession, self(), { rule_data, ?MODULE, blacklist }, "*", ["/shared/vendor/kolab/folder-type"]);
fetch_metadata(_ImapSession, _State) -> ok.

apply_if_id_matches(<<"ID">>, Data, _TriggerCommands) ->
    apply_if_found_kolab(binary:match(Data, <<"/Kolab">>));
apply_if_id_matches(Command, _Data, TriggerCommands) ->
    case lists:any(fun(T) -> Command =:= T end, TriggerCommands) of
        true -> true;
        _ -> notyet
    end.

apply_if_found_kolab(nomatch) -> true;
apply_if_found_kolab(_) -> false.

filter_folders(<<>>, State) ->
    { <<>>, State#state{ active = true } };
filter_folders(Buffer, #state{ last_chunk = LeftOvers } = State) ->
    FullBuffer = <<LeftOvers/binary, Buffer/binary>>,
    { FullLinesBuffer, LastChunk } = eimap_utils:only_full_lines(FullBuffer),
    ListResponses = binary:split(FullLinesBuffer, <<"\r\n">>, [ global ]),
    { Response, More } = filter_folders(State, ListResponses, { <<>>, true }),
    %io:format("Filtered ... ~p~n", [Response]),
    { <<Response/binary, "\r\n">>, State#state { active = More, last_chunk = LastChunk } }.

filter_folders(_State, [], Return) -> Return;
filter_folders(_State, _Folders, { Acc, false }) -> { Acc, false };
filter_folders(State, [Unfiltered|Folders], { Acc, _More }) -> filter_folders(State, Folders, filter_folder(State, Unfiltered, Acc)).

filter_folder(_State, <<>>, Acc) -> { Acc, true };
filter_folder(State, <<"* LIST ", Details/binary>> = Response, Acc) -> { filter_on_details(State, Response, Acc, Details), true };
filter_folder(State, <<"* XLIST ", Details/binary>> = Response, Acc) -> { filter_on_details(State, Response, Acc, Details), true };
filter_folder(State, <<"* LSUB ", Details/binary>> = Response, Acc) -> { filter_on_details(State, Response, Acc, Details), true };
filter_folder(#state{ tag = Tag }, Response, Acc) ->
    HasMore =
    case byte_size(Tag) =< byte_size(Response) of
        true ->
            case binary:match(Response, Tag, [{ scope, { 0, byte_size(Tag) } }]) of
                nomatch -> true;
                _ -> false % we have found our closing tag!
            end;
        false -> true
    end,
    { add_response(Response, Acc), HasMore }.

filter_on_details(#state{ blacklist = Blacklist }, Response, Acc, Details) ->
    %% first determine if we have a quoted item or a non-quoted item and start from there
    DetailsSize = byte_size(Details),
    { Quoted, Start } = case binary:at(Details, DetailsSize - 1) of $" -> { quoted, DetailsSize - 2 }; _ -> { unquoted, DetailsSize - 1 } end,
    Folder = find_folder_name(Details, Quoted, Start, Start, binary:at(Details, Start)),
    %io:format("COMPARING ~p ??? ~p~n", [Folder, in_blacklist(Folder, Blacklist)]),
    case in_blacklist(Folder, Blacklist) of
        true -> Acc;
        _ -> add_response(Response, Acc)
    end.

find_folder_name(Details, quoted, End, Start, $") ->
    binary:part(Details, Start + 1, End - Start);
find_folder_name(Details, unquoted, End, Start, $ ) ->
    binary:part(Details, Start + 1, End - Start);
find_folder_name(Details, _Quoted, _End, 0, _) ->
    Details;
find_folder_name(Details, Quoted, End, Start, _) ->
    find_folder_name(Details, Quoted, End, Start - 1, binary:at(Details, Start - 1)).

add_response(Response, <<>>) -> Response;
add_response(Response, Acc) -> <<Acc/binary, "\r\n", Response/binary>>.

in_blacklist(_Folder, undefined) -> false;
in_blacklist(_Folder, []) -> false;
in_blacklist(Folder, [{ Literal, Prefix }|List]) ->
    case Literal =:= Folder of
        true -> true;
        _ -> case binary:match(Folder, Prefix) of
                 { 0, _ } -> true;
                 _ -> in_blacklist(Folder, List)
             end
    end.
