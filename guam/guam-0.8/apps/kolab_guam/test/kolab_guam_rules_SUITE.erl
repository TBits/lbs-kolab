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

-module(kolab_guam_rules_SUITE).

% easier than exporting by name
-compile(export_all).

% required for common_test to work
-include("ct.hrl").

%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% common test callbacks %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Specify a list of all unit test functions
all() -> [
          kolab_guam_rule_filter_groupware_responsefiltering_test,
          kolab_guam_rule_filter_groupware_responsefiltering_multipacket_test
         ].

% required, but can just return Config. this is a suite level setup function.
init_per_suite(Config) ->
        Config.

% required, but can just return Config. this is a suite level tear down function.
end_per_suite(Config) ->
        Config.

% optional, can do function level setup for all functions,
% or for individual functions by matching on TestCase.
init_per_testcase(_TestCase, Config) ->
        Config.

% optional, can do function level tear down for all functions,
% or for individual functions by matching on TestCase.
end_per_testcase(_TestCase, Config) ->
        Config.

% c("apps/kolab_guam/test/kolab_guam_sup_tests.erl"). eunit:test(kolab_guam_sup_tests).

kolab_guam_rule_filter_groupware_responsefiltering_test(_TestConfig) ->
    Data = [
        {
            <<"* LIST (\\Noinferiors \\Subscribed) \"/\" INBOX\r\n* LIST (\\Subscribed) \"/\" Archive\r\n* LIST (\\Subscribed \\HasChildren) \"/\" Calendar\r\n* LIST (\\Subscribed) \"/\" \"Calendar/Personal Calendar\"\r\n* LIST (\\Subscribed) \"/\" Configuration\r\n* LIST (\\Subscribed \\HasChildren) \"/\" Contacts\r\n* LIST (\\Subscribed) \"/\" \"Contacts/Personal Contacts\"\r\n* LIST (\\Subscribed) \"/\" Drafts\r\n* LIST (\\Subscribed) \"/\" Files\r\n* LIST (\\Subscribed) \"/\" Journal\r\n* LIST (\\Subscribed) \"/\" Notes\r\n* LIST (\\Subscribed) \"/\" Sent\r\n* LIST (\\Subscribed) \"/\" Spam\r\n* LIST (\\Subscribed) \"/\" Tasks\r\n* LIST (\\Subscribed) \"/\" Trash\r\n7 OK Completed (0.000 secs 15 calls)\r\n">>,
            <<"* LIST (\\Noinferiors \\Subscribed) \"/\" INBOX\r\n* LIST (\\Subscribed) \"/\" Archive\r\n* LIST (\\Subscribed) \"/\" Drafts\r\n* LIST (\\Subscribed) \"/\" Sent\r\n* LIST (\\Subscribed) \"/\" Spam\r\n* LIST (\\Subscribed) \"/\" Trash\r\n7 OK Completed (0.000 secs 15 calls)\r\n">>
        }
    ],
    Config = {}, %%TODO?
    State = kolab_guam_rule_filter_groupware:new(Config),
    ServerConfig = kolab_guam_sup:default_imap_server_config(),
    { ok, ImapSession } = eimap:start_link(ServerConfig),
    { _, ReadyState } = kolab_guam_rule_filter_groupware:apply_to_client_message(ImapSession, <<"7 list (subscribed) \"\" \"*\" return (special-use)">>, State),
    lists:foreach(fun({ Input, Filtered }) -> { Filtered, NewState } = kolab_guam_rule_filter_groupware:apply_to_server_message(ImapSession, Input, ReadyState) end, Data).

kolab_guam_rule_filter_groupware_responsefiltering_multipacket_test(_TestConfig) ->
    Data = [
        {
            [
                <<"* LIST (\\Noinferiors \\Subscribed) \"/\" INBOX\r\n* LIST (\\Subscribed) \"/\" Archive\r\n* LIST (\\Subscribed \\HasChildren) \"/\" Calendar\r\n* LIST (\\Subscribed) \"/\" \"Calendar/Personal Calendar\"\r\n* LIST (\\Subscribed) \"/\" Configuration\r\n* LIST (\\Subscribed \\HasChildren) \"/\" Contacts\r\n* LIST (\\Subscribed) \"/\" \"Contacts/Personal Contacts\"\r\n* LIST (\\Subscribed) \"/\" Drafts\r\n* LIST (\\Subscribed) \"/\" Files\r\n* LIST (\\Subscribed) \"/\" Journal\r\n* LIST (\\Subscribed)">>,
                <<"\"/\" Notes\r\n* LIST (\\Subscribed) \"/\" Sent\r\n* LIST (\\Subscribed) \"/\" Spam\r\n* LIST (\\Subscribed) \"/\" Tasks\r\n* LIST (\\Subscribed) \"/\" Trash\r\n7 OK Completed (0.000 secs 15 calls)\r\n">>
            ],
            <<"* LIST (\\Noinferiors \\Subscribed) \"/\" INBOX\r\n* LIST (\\Subscribed) \"/\" Archive\r\n* LIST (\\Subscribed) \"/\" Drafts\r\n* LIST (\\Subscribed) \"/\" Sent\r\n* LIST (\\Subscribed) \"/\" Spam\r\n* LIST (\\Subscribed) \"/\" Trash\r\n7 OK Completed (0.000 secs 15 calls)\r\n">>
        }
    ],
    Config = {}, %%TODO?
    State = kolab_guam_rule_filter_groupware:new(Config),
    { _, ReadyState } = kolab_guam_rule_filter_groupware:apply_to_client_message(<<"7 list (subscribed) \"\" \"*\" return (special-use)">>, State),
    lists:foreach(fun({ Input, Filtered }) -> Filtered = filter_groupware_packets(ReadyState, Input, <<>>) end, Data).

filter_groupware_packets(_ReadyState, [], Buffer) -> Buffer;
filter_groupware_packets(ReadyState, [Input|More], Buffer) ->
    { Processed, State } = kolab_guam_rule_filter_groupware:apply_to_server_message(Input, ReadyState),
    filter_groupware_packets(State, More, <<Buffer/binary, Processed/binary>>).

