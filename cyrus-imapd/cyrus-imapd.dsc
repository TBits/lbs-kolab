Format: 1.0
Source: cyrus-imapd
Binary: cyrus-imapd
Architecture: any
Version: 2.5.13.36-0~kolab2
Maintainer: Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com>
Uploaders: Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com>
Homepage: http://www.cyrusimap.org/
Standards-Version: 3.9.1
Vcs-Browser: http://git.kolabsys.com/apt/cyrus-imapd/
Vcs-Git: git://git.kolabsys.com/git/apt/cyrus-imapd
Build-Depends:
    autoconf,
    automake,
    autotools-dev,
    bison,
    comerr-dev,
    debhelper (>= 5),
    flex,
    ghostscript | gs-gpl,
    groff,
    heimdal-dev,
    libdb5.1-dev | libdb-dev,
    libjansson-dev,
    libkvm-dev [kfreebsd-amd64],
    libkvm-dev [kfreebsd-i391],
    libldap2-dev,
    libpam0g-dev,
    libpcre3-dev,
    libsasl2-dev (>= 2.1.9),
    libsnmp-dev | libsnmp9-dev,
    libssl-dev,
    libtool,
    libwrap0-dev,
    libzephyr-dev,
    lsb-base,
    perl,
    pkg-config,
    po-debconf,
    tcl-dev | tcl8.3-dev,
    transfig,
    xutils-dev | xutils
Package-List:
 cyrus-imapd deb mail extra
Files:
 00000000000000000000000000000000 0 cyrus-imapd-2.5.13-36-gad62d5485.tar.gz
 00000000000000000000000000000000 0 debian.tar.gz
