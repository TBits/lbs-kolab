[@@repository_full_name@@@@_repository_status@@]
name = @@desc@@ Packages
baseurl = @@repository_base_url@@@@repository_tag_name@@/@@dist_tag@@/@@repository_status@@$basearch
enabled = @@enabled@@
priority = 60
skip_if_unavailable = 1
gpgcheck = @@gpgcheck@@
gpgkey = https://ssl.kolabsys.com/@@gpgkeyname@@.asc
@@ssl_stanza@@

[@@repository_full_name@@@@_repository_status@@-debuginfo]
name = @@desc@@ Packages - Debugging Symbols
baseurl = @@repository_base_url@@@@repository_tag_name@@/@@dist_tag@@/@@repository_status@@$basearch/debug
enabled = 0
priority = 60
skip_if_unavailable = 1
gpgcheck = @@gpgcheck@@
gpgkey = https://ssl.kolabsys.com/@@gpgkeyname@@.asc
@@ssl_stanza@@

[@@repository_full_name@@@@_repository_status@@-source]
name = @@desc@@ Packages - Sources
baseurl = @@repository_base_url@@@@repository_tag_name@@/@@dist_tag@@/@@repository_status@@SRPMS
enabled = 0
priority = 60
skip_if_unavailable = 1
gpgcheck = @@gpgcheck@@
gpgkey = https://ssl.kolabsys.com/@@gpgkeyname@@.asc
@@ssl_stanza@@
