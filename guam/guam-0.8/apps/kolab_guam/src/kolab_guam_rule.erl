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

-module(kolab_guam_rule).

-callback new(Args :: any()) -> any().
-callback applies(ConnectionDetails :: list(), Buffer :: binary(), State :: any()) -> { true, State :: any() } |
                                                                                      { false, State :: any() } |
                                                                                      { notyet, State :: any() }.
-callback apply_to_client_message(ImapSession :: pid(), Command :: binary(), State :: any()) -> { ProcessedCommand :: binary(), State :: any() }.
-callback apply_to_server_message(ImapSession :: pid(), Command :: binary(), State :: any()) -> { ProcessedCommand :: binary(), State :: any() }.
-callback imap_data(ResponseToken :: any(), Response :: any(), State :: any()) -> State ::any().
