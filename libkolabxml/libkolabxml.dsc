Format: 1.0
Source: libkolabxml
Binary: libkolabxml1v5, php-kolabformat, python-kolabformat, libkolabxml-dev
Architecture: any
Version: 1.2.0-0~kolab2
Maintainer: Kolab Systems AG <contact@kolabsystems.com>
Uploaders: Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com>
Homepage: http://git.kolab.org/libkolabxml
Standards-Version: 3.9.3
Build-Depends: cmake,
               debhelper,
               libboost-dev,
               libboost-system-dev,
               libboost-thread-dev,
               libcurl4-gnutls-dev,
               libossp-uuid-dev,
               libqt4-dev,
               libxerces-c-dev,
               php-cgi | php5-cli,
               php-dev | php5-dev,
               python-dev,
               swig (>= 2.0),
               xsdcxx
Package-List: 
 libkolabxml-dev deb libdevel optional
 libkolabxml1v5 deb libs optional
 php-kolabformat deb libs optional
 python-kolabformat deb python optional
Files: 
 00000000000000000000000000000000 0 libkolabxml-1.2.0.tar.gz
 00000000000000000000000000000000 0 debian.tar.gz
