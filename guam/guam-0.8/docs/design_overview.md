Data Types
==========

* Address: IPv4/IPv6, IP address, port
* IMAP Server: address and port of an IMAP server
* Rule Set: list of rules
* Rule: Scope, IMAP server, list of Transforms
* ScopeData record: { atom ConnectionState, address Incoming, binary Command }
* SessionState record: { socket Socket, address Incoming, eimap IMAP, [FilterData] filter_data_cache }
* FilterData: { atom Name, any Data }

Modules
=======
* kolab_guam_imap: Erlang application adapted from egara_imap, a stateful imap client
* kolab_guam_listener: Socket listener
* kolab_guam_session: Handler for a given client connection


Behaviors
=========
* Scope - used to see if a rule set matches a given session
    * matches(ScopeData) -> match
                            { match, [filter_data] }
                            unsure
                            nomatch

* Condition
    * matches(SessionState, binary Command) -> { pre, function Filter }
                                               { post, function Filter }
                                               { auth, function Filter }
                                               pass
* Filter
    * auth_command(SessionState, binary Command) -> binary NewCommand
                                               { binary NewCommand, final }
                                               drop
    * auth_response(SessionState, binary Command, binary Response) -> binary NewResponse
                                                                      { binary NewResponse, final }
                                                                      { binary NewResponse, more }
                                                                      drop
    * command(SessionState, binary Command) -> binary NewCommand
                                               { binary NewCommand, final }
                                               drop
    * response(SessionState, binary Command, binary Response) -> binary NewResponse
                                                                 { binary NewResponse, final }
                                                                 { binary NewResponse, more }
                                                                 drop


Process Hierarchy
=================
There is one supervisor for the set of Listeners.

Each configured Address results in one Listener process responsible for
connections on that Address. Each Listener holds one pre-allocated Session
process for use with the next connection.

Session processes have no supervision (a crash will represent a forced
disconnect) and are spawned by Listeners. Each Session process has an IMAP
process which communicates with the backend.


Working Data Set
================

At program start, or on reconfiguration, the following is read from configuration:

* IMAP server addresses as { atom name, imap_server Address } tuples
* atom default_imap_server, must reference a server in IMAP server addresses
* The addresses to listen on, and for each address a Listener is started which:
    * opens the socket for listening (or dies trying)
    * reads in the matching RuleSets for that address
    * optional atom default_imap_server, must reference a server in IMAP server addresses

Sessions
========
On creation of a new session due to a client connection, all auth rule sets are matched
prior to connection. If a rule set matches and identifies the IMAP server to connect to
then it is responsible for connecting to the IMAP server in question. Once connection
is established, authentication is established via the same set of auth filters.

Once the IMAP process is in the auth state, for each command the pre conditions are run,
the resulting command is sent, and the post conditions are run upon data receiption.

If connection is lost to the IMAP server, then the session also terminates immediately.

Egara Integration
=================
Sending events to egara so as to capture events as they occur in the Kolab data loss
prevention and auditing framework will be accomplished thorugh a custom lager backend
and formater. The formater will take a term and turn it into appropriate json (or simply
send it across to egara if "raw" Erlang terms are supported for input at that point),
and the backend will route the messages to egara, holding them in local storage until
successfully sent to an egara sink.
