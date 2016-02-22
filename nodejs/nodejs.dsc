Format: 1.0
Source: nodejs
Binary: nodejs-dev, nodejs, nodejs-dbg, nodejs-legacy
Architecture: any all
Version: 0.12.8-0~kolab2
Maintainer: Jeroen van Meeuwen <vanmeeuwen@kolabsys.com>
Homepage: http://nodejs.org/
Standards-Version: 3.9.5
Build-Depends: cdbs, devscripts, debhelper, dh-buildinfo, binutils, openssl (>= 1.0.0g), pkg-config, bash-completion, curl, procps, zlib1g-dev, libkvm-dev [kfreebsd-any], gyp (>= 0.1~svn1654), python, libssl-dev (>= 1.0.0g)
Package-List:
 nodejs deb web optional arch=any
 nodejs-dbg deb debug extra arch=any
 nodejs-dev deb devel extra arch=any
 nodejs-legacy deb web extra arch=all
Files:
 00000000000000000000000000000000 0 nodejs-0.12.8-stripped.tar.gz
 00000000000000000000000000000000 0 debian.tar.gz
