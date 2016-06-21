Functional description
======================
The Kolab Payload Filter (KPF), aka Guam, is responsible for sitting between a Kolab Groupware Server and a user's client software and applying a set of dynamic transformations to requests from the client and responses from the server in a fashion that is transparent to the client and generally secure.

It needs to support various matching and filtering rules which may vary based on the user's account as well as source and destination network addresses.

Use Cases
=========
* Filter all groupware folders from mail listings to allow usable and safe access to a Kolab Groupware Server over imap from clients that do not understand groupware folders.
* Deny access to files that are marked for security / privacy reasons (secret, etc.)
* Allow access to a limited set of content from outside the office and full access inside the office

Design Brief
============
The system will be written in Erlang around the following concepts.

KPF will listen on one or more network interfaces (IP address + port) to accept incoming connections from clients. Each connection will behandled in its own Erlang process, giving data separation and scalability "for free".

Rule sets form the core of the filtering logic. A rule set contains zero (a null set) or more rules in a chain, each of which may:
    * match command types and alloy/deny/filter access
        * e.g. filter out groupware folders (the primary Munich use case)
    * match path (folder, message, ..) and allow/deny/filter access
    * match message properties / tags and allow/deny/filter access based on those
    * arbitrary Erlang functions

Rule set chains are applied in first-to-last order allowing multiple transformations
in a predictable order.

Rule sets are paired with matching criterion include:
    * scope
        * default (apply to all)
        * group (accounts may belong to 0..N groups)
        * account (a specific account or a regular expression)
    * incoming (external) address the client is accessing from
    * destination (local) address the client is connecting to

When a client connects the KPF will:

    1. Load / apply matching rule sets associated with applicable addresses
    2. Perform authentication
        * may pass through a rule set first, including:
            * transformation of account name
            * transformation of account dest
            * application of white/black lists
        * authenticate against Kolab Groupware server
    3. Load all rule sets that apply to the authenticated account
    4. Each request passes through the rule sets, possibly modifying request
       and/or response

This allows behavior to be modified based on where the client is, which address they connect to, what they access and which account they authenticate to. The results of the  rule set passes are arbitrary, allowing for future expansion beyond the initial simple use case of filtering folders.

Rule sets would be stored in a <define storage location> and modified using a <web interface?>.

Initially we would implement the "bare" framework for the above and only implement the filter-groupware-folders rule. Further rule development would occur on as-needed basis.
