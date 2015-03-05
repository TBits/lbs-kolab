Format: 1.0
Source: apache2
Binary: apache2.2-common, apache2.2-bin, apache2-mpm-worker, apache2-mpm-prefork, apache2-mpm-event, apache2-mpm-itk, apache2-utils, apache2-suexec, apache2-suexec-custom, apache2, apache2-doc, apache2-prefork-dev, apache2-threaded-dev, apache2-dbg
Architecture: any all
Version: 2.2.22-13.2+deb7u3
Maintainer: Debian Apache Maintainers <debian-apache@lists.debian.org>
Uploaders: Stefan Fritsch <sf@debian.org>, Steinar H. Gunderson <sesse@debian.org>, Arno Töll <arno@debian.org>
Homepage: http://httpd.apache.org/
Standards-Version: 3.9.3
Vcs-Browser: http://anonscm.debian.org/gitweb/?p=pkg-apache/apache2.git
Vcs-Git: git://git.debian.org/git/pkg-apache/apache2.git
Build-Depends: debhelper (>= 8.9.7~), lsb-release, libaprutil1-dev (>= 1.3.4), libapr1-dev, openssl, libpcre3-dev, mawk, zlib1g-dev, libssl-dev (>= 1.0.1), sharutils, libcap-dev [linux-any], autoconf, autotools-dev
Build-Conflicts: autoconf2.13
Package-List: 
 apache2 deb httpd optional
 apache2-dbg deb debug extra
 apache2-doc deb doc optional
 apache2-mpm-event deb httpd optional
 apache2-mpm-itk deb httpd extra
 apache2-mpm-prefork deb httpd optional
 apache2-mpm-worker deb httpd optional
 apache2-prefork-dev deb httpd extra
 apache2-suexec deb httpd optional
 apache2-suexec-custom deb httpd extra
 apache2-threaded-dev deb httpd extra
 apache2-utils deb httpd optional
 apache2.2-bin deb httpd optional
 apache2.2-common deb httpd optional
Files: 
 00000000000000000000000000000000 0 httpd-2.2.22.tar.gz
 00000000000000000000000000000000 0 debian.tar.gz
