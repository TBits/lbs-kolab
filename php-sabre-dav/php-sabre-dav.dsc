Format: 1.0
Source: php-sabre-dav-2.1
Binary: php-sabre-dav-2.1
Architecture: all
Version: 2.1.11-2
Maintainer: Kolab for Debian testing <devel@lists.kolab.org>
Uploaders: hede <kolab983@der-he.de>
Homepage: http://sabre.io/dav/
Standards-Version: 3.9.6
Vcs-Git: git://anonscm.debian.org/pkg-owncloud/php-sabredav.git -b 2.1
Vcs-Browser: http://anonscm.debian.org/gitweb/?p=pkg-owncloud/php-sabredav.git
Build-Depends: debhelper (>= 8.0.0),
               help2man,
               php-codesniffer,
               php-curl | php5-curl,
               php-mbstring | php5,
               php-sabre-event,
               php-sabre-http-3,
               php-sabre-vobject-3,
               php-sqlite3 | php5-sqlite,
               phpab,
               phpunit,
               pkg-php-tools (>= 1.7~),
               python
Package-List:
 php-sabre-http-3 deb php optional arch=all
Files:
 00000000000000000000000000000000 0 sabre-http-3.0.5.tar.gz
 00000000000000000000000000000000 0 debian.tar.gz
