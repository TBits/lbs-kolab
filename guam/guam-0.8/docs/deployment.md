Deploying Guam
==============

This document covers the deployment of Guam in a Kolab environment.

Installation
------------
TBD

Running Guam
------------

Guam includes a kolab_guam binary in the bin/ directory. This binary can be used
to start, stop, restart, etc. Guam. For example, assumign kolab_guam is in your
path:

    kolab_guam start   # starts Guam in the background
    kolab_guam console # starts Guam in a foreground console
    kolab_guam ping    # determine if the server is running or not
    kolab_guam attach  # attaches to a running Guam and opens a console to it
    kolab_guam stop    # stop Guam
    kolab_guam restart # restarts Guam

The version of Guam packaged with Kolab comes with a systemd module file,
which can be used to integrate with systemd managed operating systems.

Configuration
-------------
Guam's config is stored in releases/<version#>/sys.config.

The file contains configuration for the following aspect of Guam:

    * imap_servers: The IMAP servers to connet to
    * listeners: the ports Guam should be listening on

These are all wrapped in a { kolab_guam, [ ... ] } entry in the file.

### imap_servers

imap_servers can have one or more entries in it, one for each IMAP server that
Guam may use. Each IMAP server can have the following aspects specified:

    * host: an IP address or hostname to connect to
    * port: the port to connet to
    * tls: false for no encryption, true for implicit SSL or starttls for
           the encryption to be started with STARTTLS on IMAP servers that 
           advertise that capability (NOTE: starttls not included in v0.2)

An IMAP server labeled "default" is required to exist for proper functionality.

Example:

    { imap_servers, [
                    { default, [
                                 { host, "192.168.56.101" },
                                 { port, 993 },
                                 { tls, true }
                               ]
                    },
                    { other_server, [
                                 { host, "kolab.acmeinc.com" },
                                 { port, 143 }
                                 { tls, false }
                    ]
    },


If running Guam on the same server as the IMAP backend, it is recommended
to set tls to false as encryption between Guam and the IMAP server is in that
case is superfluous and therefore simply a waste of resources.

### listeners

For each port that Guam should listen on one listener configuration must be
present. This configuration also controls which rules are applied. Each listener
is defined by a key, which is the name used in e.g. logging, and a value which
contains the configuration specifics. Example:

    { listeners, [
       { default, [
                { host, "127.0.0.1" },
                { port, 1936 },
                { imap_server, default },
                { rules, [ { filter_groupware, [] } ] },
                { tls_config, [ { certfile, "/etc/ssl/sample.pem" } ] }
            ]
        }
    }

The host entry is optional, and is used to bind the connection to a specific
network interface. Leaving it empty will cause Guam to bind to the port accross
all network interfaces available to it.

port defines the port it is listening on.

imap_server refers to the entry in the imap_servers block. If not provided, the
default entry in the imap_servers configuration is used.

rules contains the rules to apply to sessions with this listener. If not provided,
then no rules are applied. The rules are a list containing pairs of rule names
and rule configuration. In the above example, there is exactly one rule to be
applied and it has no specific configuration. A more elaborate example might be:

    { rules, [
        { filter_groupware, [] },
        { deny_access, [ "badhost.com" ] },
        { filter_users, [ "*@acme.com", { silent, true } ] }
        ]
    }

Finally, there is the tls_config. This must be provided if STARTTLS is to be
supported. (Implicit TLS is currently not supported by listeners.) The minimum
configuration provides the path to a PEM bundle, however one can also define
the path to cacerts, client certs, individuals key/cert files (e.g. not in a PEM
bundle) as well as the cyphers to be used. See this for full details of all
supported options:

    http://www.erlang.org/doc/man/ssl.html


Logging
-------

Logging is controlled with a top-level group in the group with the key "lager".
A sample configuration would look like this:

{ lager,
    [
    {
        handlers,
        [
        { lager_console_backend, debug },
        { lager_file_backend, [ { file, "log/error.log"}, { level, error } ] },
        { lager_file_backend, [ { file, "log/console.log"}, { level, debug } ] }
        ] }
    ] }

Each handler describes where the messages are routed (console, file, ...) and 
the message levels which are directed to those end points. The message levels
used in egara include: info, warn, error and debug.

See https://github.com/basho/lager for more details on lager configuration.
