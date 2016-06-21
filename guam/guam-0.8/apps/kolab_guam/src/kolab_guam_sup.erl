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

-module(kolab_guam_sup).

-behaviour(supervisor).

%% API
-export([start_link/0, default_imap_server_config/0, imap_server_config/1]).

%% Supervisor callbacks
-export([init/1]).

%% ===================================================================
%% API functions
%% ===================================================================

start_link() ->
    supervisor:start_link({local, ?MODULE}, ?MODULE, []).

default_imap_server_config() -> imap_server_config(default).

imap_server_config(DefinitionName) when is_atom(DefinitionName) ->
    ServerDefinitions = application:get_env(kolab_guam, imap_servers, []),
    proplists:get_value(DefinitionName, ServerDefinitions, []).

%% ===================================================================
%% Supervisor callbacks
%% ===================================================================

init([]) ->
    lager:debug("Creating listeners ..."),
    ListenersConfig = application:get_env(kolab_guam, listeners, []),
    Children = [ create_child(Name, ListenerConfig) || { Name, ListenerConfig } <- ListenersConfig ],
    lager:debug("We have ~p~n", [Children]),
    { ok, { { one_for_one, 5, 10}, Children } }.

create_child(Name, ListenerConfig) ->
    lager:debug("Making listener \"~p\" with ~p", [Name, ListenerConfig]),
    { Name, { kolab_guam_listener, start_link, [Name, ListenerConfig] }, permanent, 5000, supervisor, [Name] }.
