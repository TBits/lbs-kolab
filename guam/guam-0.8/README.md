Guam
====

Guam is an IMAP proxy and filter written in Erlang developed by Kolab Systems.

Information on the design, deployment, etc. of Guam can be found in the docs
directory.

Building
--------

Building guam for development is easy. First, ensure you have Erlang and make
installed. Thenn run `make deps-up` to fetch the dependencies into the build
tree, then run `make` to build Guam. Finally, you can run it easily from the
top level directory with `make run`. You will probably wish to modify the
app.config file before doing so.

To turn a build into a distributable release, go into the rel directory and
run `../rebar generate`. This will create a kolab_guam directory (or update
the contents of it if it already exists) which can be then packaged up and
used.

Getting Involved
----------------
The maintainer of Guam is Aaron Seigo <seigo@kolabsystems.com>, and here is
the [project page](https://git.kolab.org/tag/guam/). The git repository can be
found at https://git.kolab.org/diffusion/G/guam.git

Disccusion can be had on the Kolab dev list <devel@lists.kolab.org>

