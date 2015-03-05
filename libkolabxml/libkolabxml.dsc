Format: 1.0
Source: libkolabxml
Binary: libkolabxml1, php-kolabformat, python-kolabformat, libkolabxml-dev
Architecture: any
Version: 1.1~dev20140624-0~kolab1
Maintainer: Debian Kolab Maintainers <pkg-kolab-devel@lists.alioth.debian.org>
Uploaders: Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com>, Paul Klos <kolab@klos2day.nl>
Homepage: http://git.kolab.org/libkolabxml
Standards-Version: 3.9.3
Build-Depends: cmake,
               debhelper,
               libboost-dev,
               libboost-system-dev,
               libboost-thread-dev,
               libcurl4-gnutls-dev,
               libossp-uuid-dev,
               libxerces-c-dev,
               php5-cli,
               php5-dev,
               python-dev,
               swig (>= 2.0),
               xsdcxx
Package-List: 
 libkolabxml-dev deb libdevel optional
 libkolabxml1 deb libs optional
 php-kolabformat deb libs optional
 python-kolabformat deb python optional
Files: 
 00000000000000000000000000000000 0 libkolabxml-1.1.tar.gz
 00000000000000000000000000000000 0 debian.tar.gz
