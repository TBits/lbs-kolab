Format: 1.0
Source: 389-ds-base
Binary: 389-ds, 389-ds-base-libs, 389-ds-base-libs-dbg, 389-ds-base-dev, 389-ds-base, 389-ds-base-dbg
Architecture: any all
Version: 1.2.11.30-2
Maintainer: Debian 389ds Team <pkg-fedora-ds-maintainers@lists.alioth.debian.org>
Uploaders: Timo Aaltonen <tjaalton@ubuntu.com>, Krzysztof Klimonda <kklimonda@syntaxhighlighted.com>
Homepage: http://directory.fedoraproject.org
Standards-Version: 3.9.3
Vcs-Browser: http://anonscm.debian.org/gitweb/?p=pkg-fedora-ds/389-ds-base.git
Vcs-Git: git://git.debian.org/git/pkg-fedora-ds/389-ds-base.git
Build-Depends: quilt, debhelper (>= 8), dpkg-dev (>= 1.13.19), dh-autoreconf, libnspr4-dev, libnss3-dev, libsasl2-dev, libsvrcore-dev, libldap2-dev (>= 2.4.28), libicu-dev, libsnmp-dev, libdb-dev, zlib1g-dev, libbz2-dev, libssl-dev, libpam0g-dev, pkg-config, libperl-dev, libkrb5-dev, libpcre3-dev
Package-List: 
 389-ds deb net optional
 389-ds-base deb net optional
 389-ds-base-dbg deb debug extra
 389-ds-base-dev deb libdevel optional
 389-ds-base-libs deb libs optional
 389-ds-base-libs-dbg deb debug extra
Files: 
 00000000000000000000000000000000 0 389-ds-base-1.2.11.30.tar.bz2
 00000000000000000000000000000000 0 debian.tar.gz
