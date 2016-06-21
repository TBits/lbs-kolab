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

-module(kolab_guam_sup_SUITE).

% easier than exporting by name
-compile(export_all).

% required for common_test to work
-include("ct.hrl").

%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% common test callbacks %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Specify a list of all unit test functions
all() -> [imap_server_config_test, imap_server_settings_to_config_test].

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

imap_server_settings_to_config_test(_TestConfig) ->
    Configs = [
        {
            [],
            #eimap_server_config{}
        },
        {
            [ { tls, false } ],
            #eimap_server_config{ tls = false }
        },
        {
            [ { host, "192.168.56.101" }, { port, 993 }, { tls, true } ],
            #eimap_server_config{ host = "192.168.56.101", port = 993, tls = true }
        }
    ],
    lists:foreach(fun({ Config, Record }) -> Record = kolab_guam_sup:imap_server_settings_to_config(Config) end, Configs).

default_imap_server_config_test(_TestConfig) ->
    Expected = #eimap_server_config{ host = "192.168.56.102", port = 994, tls = true },
    Expected = kolab_guam_sup:default_imap_server_config().

imap_server_config_test(_TestConfig) ->
    Configs = [
        {
            test_default,
            #eimap_server_config{ host = "192.168.56.101", port = 993, tls = false }
        }
    ],
    lists:foreach(fun({ Config, Record }) -> Record = kolab_guam_sup:imap_server_config(Config) end, Configs).

