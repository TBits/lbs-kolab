Format: 1.0
Source: php-sabre-http-3
Binary: php-sabre-http-3
Architecture: all
Version: 3.0.5-6
Maintainer: Kolab for Debian <devel@lists.kolab.org>
Uploaders: Daniel Hoffend <dh@dotlan.net>
Homepage: https://github.com/fruux/sabre-http
Standards-Version: 3.9.7
Vcs-Git: git://anonscm.debian.org/pkg-php/php-sabre-http.git -b 3.0
Vcs-Browser: http://anonscm.debian.org/gitweb/?p=pkg-php/php-sabre-http.git
Build-Depends: debhelper (>= 9),
               php-codesniffer,
               php-curl | php5-curl,
               php-sabre-event,
               php-xdebug | php5-xdebug,
               phpab,
               phpunit,
               pkg-php-tools (>= 1.7~)
Package-List:
 php-sabre-http-3 deb php optional arch=all
Files:
 00000000000000000000000000000000 0 sabre-http-3.0.5.tar.gz
 00000000000000000000000000000000 0 debian.tar.gz
