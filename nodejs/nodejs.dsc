-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA256

Format: 3.0 (quilt)
Source: nodejs
Binary: nodejs-dev, nodejs, nodejs-dbg, nodejs-legacy
Architecture: any all
Version: 0.10.29~dfsg-1~bpo70+1
Maintainer: Debian Javascript Maintainers <pkg-javascript-devel@lists.alioth.debian.org>
Uploaders: Jérémy Lal <kapouer@melix.org>, Jonas Smedegaard <dr@jones.dk>
Homepage: http://nodejs.org/
Standards-Version: 3.9.5
Vcs-Browser: http://anonscm.debian.org/gitweb/?p=collab-maint/nodejs.git
Vcs-Git: git://anonscm.debian.org/collab-maint/nodejs.git
Build-Depends: cdbs, devscripts, debhelper, dh-buildinfo, binutils, openssl (>= 1.0.0g), pkg-config, bash-completion, curl, procps, zlib1g-dev, libkvm-dev [kfreebsd-any], gyp (>= 0.1~svn1654), python, libv8-3.14-dev (>= 3.7), libssl-dev (>= 1.0.0g), libc-ares-dev (>= 1.7.5), ca-certificates
Package-List:
 nodejs deb web optional arch=any
 nodejs-dbg deb debug extra arch=any
 nodejs-dev deb devel extra arch=any
 nodejs-legacy deb web extra arch=all
Checksums-Sha1:
 844db8f427bdc58a11f7f657de6a4c87b5d2566e 6082803 nodejs_0.10.29~dfsg.orig.tar.gz
 fdcc694b5776b0affa44bd14bebebe92036482e1 40000 nodejs_0.10.29~dfsg-1~bpo70+1.debian.tar.xz
Checksums-Sha256:
 9968cb38781331a517def6ac039da74e9f0aab8f9fee433672ead73b0ae562d3 6082803 nodejs_0.10.29~dfsg.orig.tar.gz
 e4a6ae003d1e261d93c791fb989823ea94af437dac5c2118e26b959b2e57578d 40000 nodejs_0.10.29~dfsg-1~bpo70+1.debian.tar.xz
Files:
 4a492ee3329f1f3a8a5e978331f3cd7c 6082803 nodejs_0.10.29~dfsg.orig.tar.gz
 6a3dacead27b7f746b7e0d95ae7ffb88 40000 nodejs_0.10.29~dfsg-1~bpo70+1.debian.tar.xz

-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1

iQIcBAEBCAAGBQJT3ZQaAAoJEI7tzBuqHzL/UbMQAL6Dl5JwdH5SuqbyivGixPOW
aqboxIgcIAmHfiFdCi7aCh7f509jmAsRfDibx/wdnYSJ3fbCsLcEBztvQp1zThOP
uRi+bVCTibys5OK4RJmPHl0IsB00Q/XAVxrd/UTh+fMJQwrsPJh0PfZkHJnBWsvX
xSupKfxIQHuVjLeyciv2fkVcuZNx9PYPoPjCi5T//SOQR3lFXYJdtBQJtQZtmyCU
DxTxkUTQRGaMoDzBSIa2Bn5JtieIW+XgbtbCjKkE/5e46IWLYuHLKl376pQUjsG0
+KVdD4bm+PegPmkK53/R6J1IvRwcLfrGM9Bw+UzeMjwguwDmA+Z0GFtlMbSks4xl
P5D/iw/SG+/o2/Q/RWFcofK7zrEJpCiKuedcgPp2JYqWE0/dMAv5f6I1OU2i8xbA
wElBjtWNOrq6YRpErGqXPpsiyPmAZzR51UVXVe91SWL5D5otyG0IH19tghTxqX7m
iybPfsQvpGCocis0JE9idXQQNzJG+pSMWyzhtNr9DTOEJlaZuN41kbhBxB0ldQOk
0JvBYEVqikGV6nIyZcAWDHHvvDocrqEzNQ/kCl5BtBnwMQasW7gsE5W/zS3bxB6m
w59vyrqXWvkCszl51IeSqj/j+T5uNTYyY2GQOTuErSerqoNIPyb4fuMaNTvbZhfN
f1dcpQAzDy0QtxI7SUtz
=eMo8
-----END PGP SIGNATURE-----
