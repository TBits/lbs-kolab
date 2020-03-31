%define php_name ZendFramework
#define posttag .PL1

%if 0%{?suse_version}
%global php php5
%else
%global php php
%endif


Summary:         Leading open-source PHP framework
Name:            php-ZendFramework
Version:         1.12.5
Release:         2.4%{?dist}.kolab_wf

License:         BSD
Group:           Development/Libraries
Source0:         http://framework.zend.com/releases/%{php_name}-%{version}%{?posttag}/%{php_name}-%{version}%{?posttag}.tar.gz
Source1:         README.fedora
URL:             http://framework.zend.com/

BuildArch:       noarch

Requires: php-bcmath
# The following are provided by php-common:
# Requires: php-ctype
# Requires: php-curl
# Requires: php-dom
# Requires: php-hash
# Requires: php-iconv
# Requires: php-json
# Requires: php-pcre
# Requires: php-reflection
# Requires: php-session
# Requires: php-simplexml
# Requires: php-spl
# Requires: php-zlib

# This provides php-posix
%if 0%{?suse_version}
Requires: php-posix
%else
Requires: php-process
%endif

# php-dom is provided by php-xml
Requires: php-xml

# missing for Http_Client
# Requires: php-mime_magic

# Needed after the removal of the tests subpackage
Provides:  %{name}-tests = %{version}-%{release}
Obsoletes: %{name}-tests < 1.9.6-2

# Gdata moved back into the main package
Provides:  %{name}-Gdata = %{version}-%{release}
Obsoletes: %{name}-Gdata < 1.12.0-1

%description
Extending the art & spirit of PHP, Zend Framework is based on simplicity,
object-oriented best practices, corporate friendly licensing, and a rigorously
tested agile code base. Zend Framework is focused on building more secure,
reliable, and modern Web 2.0 applications & web services, and consuming widely
available APIs from leading vendors like Google, Amazon, Yahoo!, Flickr, as
well as API providers and catalogers like StrikeIron and ProgrammableWeb.


%package demos
Summary:  Demos for the Zend Framework
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description demos
This package includes Zend Framework demos for the Feeds, Gdata, Mail, OpenId,
Pdf, Search-Lucene and Services sub packages.


%package extras
Summary:  Zend Framework Extras (ZendX)
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Provides: %{name}-ZendX = %{version}-%{release}

%description extras
This package includes the ZendX libraries.


%package full
Summary:  Meta package to install full Zend Framework
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-extras = %{version}-%{release}
Requires: %{name}-Auth-Adapter-Ldap = %{version}-%{release}
Requires: %{name}-Cache-Backend-Apc = %{version}-%{release}
Requires: %{name}-Cache-Backend-Memcached = %{version}-%{release}
Requires: %{name}-Cache-Backend-Libmemcached = %{version}-%{release}
Requires: %{name}-Captcha = %{version}-%{release}
Requires: %{name}-Dojo = %{version}-%{release}
Requires: %{name}-Db-Adapter-Mysqli = %{version}-%{release}
Requires: %{name}-Db-Adapter-Firebird = %{version}-%{release}
Requires: %{name}-Db-Adapter-Pdo = %{version}-%{release}
Requires: %{name}-Db-Adapter-Pdo-Mssql = %{version}-%{release}
Requires: %{name}-Db-Adapter-Pdo-Mysql = %{version}-%{release}
Requires: %{name}-Db-Adapter-Pdo-Pgsql = %{version}-%{release}
Requires: %{name}-Feed = %{version}-%{release}
Requires: %{name}-Ldap = %{version}-%{release}
Requires: %{name}-Pdf = %{version}-%{release}
Requires: %{name}-Search-Lucene = %{version}-%{release}
Requires: %{name}-Serializer-Adapter-Igbinary = %{version}-%{release}
Requires: %{name}-Services = %{version}-%{release}
Requires: %{name}-Soap = %{version}-%{release}

%description full
This package is a meta package designed to track in all subpackages and install
the full Zend Framework


%package Auth-Adapter-Ldap
Summary:  Zend Framework LDAP Authentication Adapter
Group:    Development/Libraries
Requires: %{name}-Ldap = %{version}-%{release}

%description Auth-Adapter-Ldap
This package contains the authentication adapter needed to operate against LDAP
directories.


%package Cache-Backend-Apc
Summary:  Zend Framework APC cache backend
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-pecl-apc

%description Cache-Backend-Apc
This package contains the backend for Zend_Cache to store and retrieve data via
APC.


%package Cache-Backend-Memcached
Summary:  Zend Framework memcache cache backend
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-pecl-memcache

%description Cache-Backend-Memcached
This package contains the back end for Zend_Cache to store and retrieve data
via memcache.


%package Cache-Backend-Libmemcached
Summary:  Zend Framework libmemcache cache backend
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-pecl-memcached

%description Cache-Backend-Libmemcached
This package contains the back end for Zend_Cache to store and retrieve data
via memcache.


# %package Cache-Backend-Sqlite
# Summary:  Zend Framework sqlite back end
# Group:    Development/Libraries
# Requires: %{name} = %{version}-%{release}
# Requires: php-sqlite # Not available in Fedora's PHP

# %description Cache-Backend-Sqlite
# This package contains the back end for Zend_Cache to store and retrieve data
# via sqlite databases.


%package Captcha
Summary:  Zend Framework CAPTCHA component
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-Services = %{version}-%{release}
Requires: php-gd

%description Captcha
This package contains the Zend Framework CAPTCHA extension.


%package Dojo
Summary:  Zend Framework Dojo Toolkit integration component
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: dojo

%description Dojo
This package contains the Zend Framework Dojo Toolkit component.


%package Db-Adapter-Mysqli
Summary:  Zend Framework database adapter for mysqli
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-mysqli

%description Db-Adapter-Mysqli
This package contains the files for Zend Framework necessary to connect to a
MySQL server via mysqli connector.


# %package Db-Adapter-Db2
# Summary:  Zend Framework database adapter for DB2
# Group:    Development/Libraries
# Requires: %{name} = %{version}-%{release}
# Requires: php-ibm_db2 # Not available in Fedora's PHP

# %description Db-Adapter-Db2
# This package contains the files for Zend Framework necessary to connect to an
# IBM DB2 database.


%package Db-Adapter-Firebird
Summary:  Zend Framework database adapter for InterBase
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-interbase

%description Db-Adapter-Firebird
This package contains the files for Zend Framework necessary to connect to a
Firebird/InterBase database.


# %package Db-Adapter-Oracle
# Summary:  Zend Framework database adapter for Oracle
# Group:    Development/Libraries
# Requires: %{name} = %{version}-%{release}
# Requires: php-oci8 # Not available in Fedora's PHP

# %description Db-Adapter-Oracle
# This package contains the files for Zend Framework necessary to connect to an
# Oracle database.

%package Db-Adapter-Pdo
Summary:  Zend Framework database adapter for PDO
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-pdo

%description Db-Adapter-Pdo
This package contains the files for Zend Framework necessary to connect to
databases using the PDO Adapter.


# php-pecl-PDO_IBM not available for Fedora
# %package Db-Adapter-Pdo-Ibm
# Summary:  Zend Framework database adapter for IBM PDO
# Group:    Development/Libraries
# Requires: %{name} = %{version}-%{release}
# Requires: %{name}-Db-Adapter-Pdo = %{version}-%{release}
# Requires: php-pecl-PDO_IBM
#
# %description Db-Adapter-Pdo-Ibm
# This package contains the files for Zend Framework necessary to connect to IBM
# databases using the IBM PDO Adapter.


%package Db-Adapter-Pdo-Mssql
Summary:  Zend Framework database adapter for MS SQL PDO
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-Db-Adapter-Pdo = %{version}-%{release}
Requires: php-mssql

%description Db-Adapter-Pdo-Mssql
This package contains the files for Zend Framework necessary to connect to MS 
SQL databases using the MS SQL PDO Adapter.


%package Db-Adapter-Pdo-Mysql
Summary:  Zend Framework database adapter for MySQL PDO
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-Db-Adapter-Pdo = %{version}-%{release}
Requires: php-mysqlnd

%description Db-Adapter-Pdo-Mysql
This package contains the files for Zend Framework necessary to connect to MySQL
databases using the MySQL PDO Adapter.


%package Db-Adapter-Pdo-Pgsql
Summary:  Zend Framework database adapter for PgSQL PDO
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-Db-Adapter-Pdo = %{version}-%{release}
Requires: php-pgsql

%description Db-Adapter-Pdo-Pgsql
This package contains the files for Zend Framework necessary to connect to PgSQL
databases using the PgSQL PDO Adapter.


%package Feed
Summary:  Live syndication feeds helper
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-mbstring

%description Feed
This component provides a very simple way to work with live syndicated feeds.

* consumes RSS and Atom feeds
* provides utilities for discovering feed links
* imports feeds from multiple sources
* providers feed building and posting operations


%package Ldap
Summary:  Basic LDAP operations API
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-ldap

%description Ldap
Zend_Ldap is a class for performing LDAP operations including but not limited
to binding, searching and modifying entries in an LDAP directory.


%package Pdf
Summary:  PDF file handling helper
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-gd

%description Pdf
Portable Document Format (PDF) from Adobe is the de facto standard for
cross-platform rich documents. Now, PHP applications can create or read PDF
documents on the fly, without the need to call utilities from the shell, depend
on PHP extensions, or pay licensing fees. Zend_Pdf can even modify existing PDF
documents.

* supports Adobe PDF file format
* parses PDF structure and provides access to elements
* creates or modifies PDF documents
* utilizes memory efficiently


%package Search-Lucene
Summary:  Apache Lucene engine PHP port
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
# php-pecl-bitset is not available but this is an optional requirement
# Requires: php-bitset

%description Search-Lucene
The Apache Lucene engine is a powerful, feature-rich Java search engine that is
flexible about document storage and supports many complex query
types. Zend_Search_Lucene is a port of this engine written entirely in PHP 5.

* allows PHP-powered websites to leverage powerful search capabilities without
  the need for web services or Java
* provides binary compatibility with Apache Lucene
* matches Apache Lucene in performance


%package Serializer-Adapter-Igbinary
Summary:  Drop-in replacement for the standard PHP serializer
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-pecl-igbinary

%description Serializer-Adapter-Igbinary
Igbinary is Open Source Software released by Sulake Dynamoid Oy. It's a drop-in
replacement for the standard PHP serializer. Instead of time and space
consuming textual representation, igbinary stores PHP data structures in a
compact binary form. Savings are significant when using memcached or similar
memory based storages for serialized data. 


%package Services
Summary:  Web service APIs for a number of providers
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-Soap = %{version}-%{release}
Requires: php-mcrypt

%description Services
This package contains web service client APIs for the following services:

- Akismet
- Amazon (including EC2, S3)
- Audioscrobbler
- del.icio.us
- Developer Garden
- eBay
- Flickr
- LiveDocx
- Nirvanix
- Rackspace
- ReCaptcha
- Various URL Shortener services
- SlideShare
- SqlAzure
- StrikeIron
- Technorati
- Twitter
- Windows Azure
- Yahoo!


%package Soap
Summary:  SOAP web services server part helper
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-soap

%description Soap
Zend_Soap_Server class is intended to simplify Web Services server part
development for PHP programmers.

It may be used in WSDL or non-WSDL mode, and using classes or functions to
define Web Service API.

When Zend_Soap_Server component works in the WSDL mode, it uses already
prepared WSDL document to define server object behavior and transport layer
options.

WSDL document may be auto-generated with functionality provided by
Zend_Soap_AutoDiscovery component or should be constructed manually using
Zend_Soap_Wsdl class or any other XML generating tool.

If the non-WSDL mode is used, then all protocol options have to be set using
options mechanism.


%prep
%setup -qn %{php_name}-%{version}%{?posttag}
cp -p %{SOURCE1} .


%build
find . -type f -perm /111 \
  -fprint executables -exec %{__chmod} -x '{}' \; >/dev/null

find . -type f -name \*.sh \
  -fprint valid_executables -exec %{__chmod} +x '{}' \; >/dev/null

cat executables valid_executables|sort|uniq -u > invalid_executables


%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{php}

# remove cruft that somehow slipped into the tarball
rm -f library/Zend/.Version.php.un~

cp -pr library/Zend $RPM_BUILD_ROOT%{_datadir}/%{php}
cp -pr demos/Zend $RPM_BUILD_ROOT%{_datadir}/%{php}/Zend/demos

# ZendX
cd extras
cp -pr library/ZendX $RPM_BUILD_ROOT%{_datadir}/%{php}
cd ..

cp -pr bin/zf.{php,sh} \
  $RPM_BUILD_ROOT%{_datadir}/%{php}/Zend
mkdir -p $RPM_BUILD_ROOT%{_bindir}
ln -s %{_datadir}/%{php}/Zend/zf.sh \
  $RPM_BUILD_ROOT%{_bindir}/zf


%clean
%{__rm} -rf $RPM_BUILD_ROOT


%files
%doc LICENSE.txt DEVELOPMENT_README.md INSTALL.md README.md README-GIT.md
%doc README.fedora
%{_bindir}/zf
# we list all files explicitly to find out what's new in future releases more
# easily
%if 0%{?suse_version}
%dir %{_datadir}/%{php}
%dir %{_datadir}/%{php}/ZendX/Db
%dir %{_datadir}/%{php}/ZendX/Db/Adapter
%dir %{_datadir}/%{php}/ZendX/Db/Statement
%endif

%dir %{_datadir}/%{php}/Zend
%{_datadir}/%{php}/Zend/zf.php
%{_datadir}/%{php}/Zend/zf.sh
%{_datadir}/%{php}/Zend/Acl
%{_datadir}/%{php}/Zend/Acl.php
%{_datadir}/%{php}/Zend/Amf
%{_datadir}/%{php}/Zend/Application
%{_datadir}/%{php}/Zend/Application.php
%{_datadir}/%{php}/Zend/Auth
%exclude %{_datadir}/%{php}/Zend/Auth/Adapter/Ldap.php
%{_datadir}/%{php}/Zend/Auth.php
%{_datadir}/%{php}/Zend/Barcode
%{_datadir}/%{php}/Zend/Barcode.php
%{_datadir}/%{php}/Zend/Cache
%exclude %{_datadir}/%{php}/Zend/Cache/Backend/Apc.php
%exclude %{_datadir}/%{php}/Zend/Cache/Backend/Memcached.php
%exclude %{_datadir}/%{php}/Zend/Cache/Backend/Libmemcached.php
%{_datadir}/%{php}/Zend/Cache.php
%{_datadir}/%{php}/Zend/Cloud
%{_datadir}/%{php}/Zend/CodeGenerator
%{_datadir}/%{php}/Zend/Config
%{_datadir}/%{php}/Zend/Config.php
%{_datadir}/%{php}/Zend/Console
%{_datadir}/%{php}/Zend/Controller
%{_datadir}/%{php}/Zend/Crypt
%{_datadir}/%{php}/Zend/Crypt.php
%{_datadir}/%{php}/Zend/Currency
%{_datadir}/%{php}/Zend/Currency.php
%{_datadir}/%{php}/Zend/Date
%{_datadir}/%{php}/Zend/Date.php
%{_datadir}/%{php}/Zend/Db
%exclude %{_datadir}/%{php}/Zend/Db/Adapter/Db2.php
%exclude %{_datadir}/%{php}/Zend/Db/Adapter/Db2
%exclude %{_datadir}/%{php}/Zend/Db/Statement/Db2.php
%exclude %{_datadir}/%{php}/Zend/Db/Statement/Db2
%exclude %{_datadir}/%{php}/Zend/Db/Adapter/Mysqli.php
%exclude %{_datadir}/%{php}/Zend/Db/Adapter/Mysqli
%exclude %{_datadir}/%{php}/Zend/Db/Statement/Mysqli.php
%exclude %{_datadir}/%{php}/Zend/Db/Statement/Mysqli
%exclude %{_datadir}/%{php}/Zend/Db/Adapter/Oracle.php
%exclude %{_datadir}/%{php}/Zend/Db/Adapter/Oracle
%exclude %{_datadir}/%{php}/Zend/Db/Statement/Oracle.php
%exclude %{_datadir}/%{php}/Zend/Db/Statement/Oracle
%exclude %{_datadir}/%{php}/Zend/Db/Adapter/Pdo
%exclude %{_datadir}/%{php}/Zend/Db/Statement/Pdo.php
%exclude %{_datadir}/%{php}/Zend/Db/Statement/Pdo
%{_datadir}/%{php}/Zend/Db.php
%{_datadir}/%{php}/Zend/Debug.php
%{_datadir}/%{php}/Zend/Dom
%{_datadir}/%{php}/Zend/Exception.php
%{_datadir}/%{php}/Zend/EventManager
%{_datadir}/%{php}/Zend/File
%{_datadir}/%{php}/Zend/Filter
%{_datadir}/%{php}/Zend/Filter.php
%{_datadir}/%{php}/Zend/Form
%{_datadir}/%{php}/Zend/Form.php
%{_datadir}/%{php}/Zend/Gdata
%{_datadir}/%{php}/Zend/Gdata.php
%{_datadir}/%{php}/Zend/Http
%{_datadir}/%{php}/Zend/Json
%{_datadir}/%{php}/Zend/Json.php
%{_datadir}/%{php}/Zend/Layout
%{_datadir}/%{php}/Zend/Layout.php
%{_datadir}/%{php}/Zend/Loader
%{_datadir}/%{php}/Zend/Loader.php
%{_datadir}/%{php}/Zend/Locale
%{_datadir}/%{php}/Zend/Locale.php
%{_datadir}/%{php}/Zend/Log
%{_datadir}/%{php}/Zend/Log.php
%{_datadir}/%{php}/Zend/Mail
%{_datadir}/%{php}/Zend/Mail.php
%{_datadir}/%{php}/Zend/Markup
%{_datadir}/%{php}/Zend/Markup.php
%{_datadir}/%{php}/Zend/Measure
%{_datadir}/%{php}/Zend/Memory
%{_datadir}/%{php}/Zend/Memory.php
%{_datadir}/%{php}/Zend/Mime
%{_datadir}/%{php}/Zend/Mime.php
%{_datadir}/%{php}/Zend/Mobile
%{_datadir}/%{php}/Zend/Navigation
%{_datadir}/%{php}/Zend/Navigation.php
%{_datadir}/%{php}/Zend/Oauth
%{_datadir}/%{php}/Zend/Oauth.php
%{_datadir}/%{php}/Zend/OpenId
%{_datadir}/%{php}/Zend/OpenId.php
%{_datadir}/%{php}/Zend/Queue.php
%{_datadir}/%{php}/Zend/Queue
%{_datadir}/%{php}/Zend/Paginator
%{_datadir}/%{php}/Zend/Paginator.php
%{_datadir}/%{php}/Zend/ProgressBar
%{_datadir}/%{php}/Zend/ProgressBar.php
%{_datadir}/%{php}/Zend/Reflection
%{_datadir}/%{php}/Zend/Registry.php
%{_datadir}/%{php}/Zend/Rest
%{_datadir}/%{php}/Zend/Server
%{_datadir}/%{php}/Zend/Service
%exclude %{_datadir}/%{php}/Zend/Service/Akismet.php
%exclude %{_datadir}/%{php}/Zend/Service/Amazon.php
%exclude %{_datadir}/%{php}/Zend/Service/Amazon
%exclude %{_datadir}/%{php}/Zend/Service/Audioscrobbler.php
%exclude %{_datadir}/%{php}/Zend/Service/Delicious.php
%exclude %{_datadir}/%{php}/Zend/Service/Delicious
%exclude %{_datadir}/%{php}/Zend/Service/DeveloperGarden
%exclude %{_datadir}/%{php}/Zend/Service/Ebay
%exclude %{_datadir}/%{php}/Zend/Service/Flickr.php
%exclude %{_datadir}/%{php}/Zend/Service/Flickr
%exclude %{_datadir}/%{php}/Zend/Service/LiveDocx.php
%exclude %{_datadir}/%{php}/Zend/Service/LiveDocx
%exclude %{_datadir}/%{php}/Zend/Service/Rackspace
%exclude %{_datadir}/%{php}/Zend/Service/ReCaptcha.php
%exclude %{_datadir}/%{php}/Zend/Service/ReCaptcha
%exclude %{_datadir}/%{php}/Zend/Service/ShortUrl
%exclude %{_datadir}/%{php}/Zend/Service/SlideShare.php
%exclude %{_datadir}/%{php}/Zend/Service/SlideShare
%exclude %{_datadir}/%{php}/Zend/Service/SqlAzure
%exclude %{_datadir}/%{php}/Zend/Service/StrikeIron.php
%exclude %{_datadir}/%{php}/Zend/Service/StrikeIron
%exclude %{_datadir}/%{php}/Zend/Service/Technorati.php
%exclude %{_datadir}/%{php}/Zend/Service/Technorati
%exclude %{_datadir}/%{php}/Zend/Service/Twitter.php
%exclude %{_datadir}/%{php}/Zend/Service/Twitter
%exclude %{_datadir}/%{php}/Zend/Service/WindowsAzure
%exclude %{_datadir}/%{php}/Zend/Service/Yahoo.php
%exclude %{_datadir}/%{php}/Zend/Service/Yahoo
%{_datadir}/%{php}/Zend/Serializer
%{_datadir}/%{php}/Zend/Serializer.php
%exclude %{_datadir}/%{php}/Zend/Serializer/Adapter/Igbinary.php
%{_datadir}/%{php}/Zend/Session
%{_datadir}/%{php}/Zend/Session.php
%{_datadir}/%{php}/Zend/Stdlib
%{_datadir}/%{php}/Zend/Tag
%{_datadir}/%{php}/Zend/Test
%{_datadir}/%{php}/Zend/Text
%{_datadir}/%{php}/Zend/TimeSync
%{_datadir}/%{php}/Zend/TimeSync.php
%{_datadir}/%{php}/Zend/Tool
%{_datadir}/%{php}/Zend/Translate
%{_datadir}/%{php}/Zend/Translate.php
%{_datadir}/%{php}/Zend/Uri
%{_datadir}/%{php}/Zend/Uri.php
%{_datadir}/%{php}/Zend/Validate
%{_datadir}/%{php}/Zend/Validate.php
%{_datadir}/%{php}/Zend/Version.php
%{_datadir}/%{php}/Zend/View
%{_datadir}/%{php}/Zend/View.php
%{_datadir}/%{php}/Zend/Wildfire
%{_datadir}/%{php}/Zend/Xml
%{_datadir}/%{php}/Zend/XmlRpc

%files demos
%{_datadir}/%{php}/Zend/demos
%doc LICENSE.txt

%files extras
%{_datadir}/%{php}/ZendX
%exclude %{_datadir}/%{php}/ZendX/Db
%doc LICENSE.txt

%files full
%doc LICENSE.txt

%files Auth-Adapter-Ldap
%{_datadir}/%{php}/Zend/Auth/Adapter/Ldap.php
%doc LICENSE.txt

%files Cache-Backend-Apc
%{_datadir}/%{php}/Zend/Cache/Backend/Apc.php
%doc LICENSE.txt

%files Cache-Backend-Memcached
%{_datadir}/%{php}/Zend/Cache/Backend/Memcached.php
%doc LICENSE.txt

%files Cache-Backend-Libmemcached
%{_datadir}/%{php}/Zend/Cache/Backend/Libmemcached.php
%doc LICENSE.txt

%files Captcha
%{_datadir}/%{php}/Zend/Captcha
%doc LICENSE.txt

%files Db-Adapter-Mysqli
%{_datadir}/%{php}/Zend/Db/Adapter/Mysqli.php
%{_datadir}/%{php}/Zend/Db/Adapter/Mysqli
%{_datadir}/%{php}/Zend/Db/Statement/Mysqli.php
%{_datadir}/%{php}/Zend/Db/Statement/Mysqli
%doc LICENSE.txt

# php-ibm_db2 not available for Fedora
# %files Db-Adapter-Db2
# %{_datadir}/%{php}/Zend/Db/Adapter/Db2.php
# %{_datadir}/%{php}/Zend/Db/Adapter/Db2
# %{_datadir}/%{php}/Zend/Db/Statement/Db2.php
# %{_datadir}/%{php}/Zend/Db/Statement/Db2
# %doc LICENSE.txt

%files Db-Adapter-Firebird
%{_datadir}/%{php}/ZendX/Db/Adapter/Firebird.php
%{_datadir}/%{php}/ZendX/Db/Adapter/Firebird
%{_datadir}/%{php}/ZendX/Db/Statement/Firebird.php
%{_datadir}/%{php}/ZendX/Db/Statement/Firebird
%doc LICENSE.txt

# php-oci8 not available for Fedora
# %files Db-Adapter-Oracle
# %{_datadir}/%{php}/Zend/Db/Adapter/Oracle.php
# %{_datadir}/%{php}/Zend/Db/Adapter/Oracle
# %{_datadir}/%{php}/Zend/Db/Statement/Oracle.php
# %{_datadir}/%{php}/Zend/Db/Statement/Oracle
# %doc LICENSE.txt

%files Db-Adapter-Pdo
%{_datadir}/%{php}/Zend/Db/Adapter/Pdo
%{_datadir}/%{php}/Zend/Db/Statement/Pdo.php
%{_datadir}/%{php}/Zend/Db/Statement/Pdo
%exclude %{_datadir}/%{php}/Zend/Db/Adapter/Pdo/Ibm.php
%exclude %{_datadir}/%{php}/Zend/Db/Adapter/Pdo/Ibm
%exclude %{_datadir}/%{php}/Zend/Db/Statement/Pdo/Ibm.php
%exclude %{_datadir}/%{php}/Zend/Db/Statement/Pdo/Oci.php
%exclude %{_datadir}/%{php}/Zend/Db/Adapter/Pdo/Mssql.php
%exclude %{_datadir}/%{php}/Zend/Db/Adapter/Pdo/Mysql.php
%exclude %{_datadir}/%{php}/Zend/Db/Adapter/Pdo/Oci.php
%exclude %{_datadir}/%{php}/Zend/Db/Adapter/Pdo/Pgsql.php
%doc LICENSE.txt

# php-pecl-PDO_IBM not available for Fedora
# %files Db-Adapter-Pdo-Ibm
# %{_datadir}/%{php}/Zend/Db/Adapter/Pdo/Ibm.php
# %{_datadir}/%{php}/Zend/Db/Adapter/Pdo/Ibm
# %{_datadir}/%{php}/Zend/Db/Statement/Pdo/Ibm.php
# %doc LICENSE.txt

%files Db-Adapter-Pdo-Mssql
%{_datadir}/%{php}/Zend/Db/Adapter/Pdo/Mssql.php
%doc LICENSE.txt

%files Db-Adapter-Pdo-Mysql
%{_datadir}/%{php}/Zend/Db/Adapter/Pdo/Mysql.php
%doc LICENSE.txt

%files Db-Adapter-Pdo-Pgsql
%{_datadir}/%{php}/Zend/Db/Adapter/Pdo/Pgsql.php
%doc LICENSE.txt

%files Dojo
%{_datadir}/%{php}/Zend/Dojo.php
%{_datadir}/%{php}/Zend/Dojo
%doc LICENSE.txt

%files Feed
%{_datadir}/%{php}/Zend/Feed.php
%{_datadir}/%{php}/Zend/Feed
%doc LICENSE.txt

%files Ldap
%{_datadir}/%{php}/Zend/Ldap.php
%{_datadir}/%{php}/Zend/Ldap
%doc LICENSE.txt

%files Pdf
%{_datadir}/%{php}/Zend/Pdf.php
%{_datadir}/%{php}/Zend/Pdf
%doc LICENSE.txt

%files Search-Lucene
%{_datadir}/%{php}/Zend/Search
%doc LICENSE.txt

%files Serializer-Adapter-Igbinary
%{_datadir}/%{php}/Zend/Serializer/Adapter/Igbinary.php
%doc LICENSE.txt

%files Services
%{_datadir}/%{php}/Zend/Service/Akismet.php
%{_datadir}/%{php}/Zend/Service/Amazon.php
%{_datadir}/%{php}/Zend/Service/Amazon
%{_datadir}/%{php}/Zend/Service/Audioscrobbler.php
%{_datadir}/%{php}/Zend/Service/Delicious.php
%{_datadir}/%{php}/Zend/Service/Delicious
%{_datadir}/%{php}/Zend/Service/DeveloperGarden
%{_datadir}/%{php}/Zend/Service/Ebay
%{_datadir}/%{php}/Zend/Service/Flickr.php
%{_datadir}/%{php}/Zend/Service/Flickr
%{_datadir}/%{php}/Zend/Service/LiveDocx.php
%{_datadir}/%{php}/Zend/Service/LiveDocx
%{_datadir}/%{php}/Zend/Service/Rackspace
%{_datadir}/%{php}/Zend/Service/ReCaptcha.php
%{_datadir}/%{php}/Zend/Service/ReCaptcha
%{_datadir}/%{php}/Zend/Service/ShortUrl
%{_datadir}/%{php}/Zend/Service/SlideShare.php
%{_datadir}/%{php}/Zend/Service/SlideShare
%{_datadir}/%{php}/Zend/Service/SqlAzure
%{_datadir}/%{php}/Zend/Service/StrikeIron.php
%{_datadir}/%{php}/Zend/Service/StrikeIron
%{_datadir}/%{php}/Zend/Service/Technorati.php
%{_datadir}/%{php}/Zend/Service/Technorati
%{_datadir}/%{php}/Zend/Service/Twitter.php
%{_datadir}/%{php}/Zend/Service/Twitter
%{_datadir}/%{php}/Zend/Service/WindowsAzure
%{_datadir}/%{php}/Zend/Service/Yahoo.php
%{_datadir}/%{php}/Zend/Service/Yahoo
%doc LICENSE.txt

%files Soap
%{_datadir}/%{php}/Zend/Soap
%doc LICENSE.txt


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 27 2014 Felix Kaechele <felix@fetzig.org> - 1.12.5-1
- update to 1.12.5
- fixes http://framework.zend.com/security/advisory/ZF2014-01
- fixes http://framework.zend.com/security/advisory/ZF2014-02
- removed: InfoCards, Services/Nirvanix

* Sun Dec 22 2013 Felix Kaechele <felix@fetzig.org> - 1.12.3-3
- remove direct dependency on PHP
- See http://fedoraproject.org/wiki/Packaging:PHP#Apache_requirement

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 15 2013 Felix Kaechele <heffer@fedoraproject.org> - 1.12.3-1
- update to 1.12.3
- more 3rdparty API fixes
- full changelog http://framework.zend.com/changelog/1.12.3

* Mon Mar 04 2013 Felix Kaechele <heffer@fedoraproject.org> - 1.12.2-1
- update to 1.12.2
- fixes Twitter API
- 50+ other bugfixes
- full changelog http://framework.zend.com/changelog/1.12.2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 27 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.12.1-1
- update to 1.12.1
- full changelog http://framework.zend.com/changelog/1.12.1
- fixes CVE-2012-5657 aka ZF2012-05: Potential XML eXternal Entity injection
  vectors in Zend Framework 1 Zend_Feed component

* Thu Aug 30 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.12.0-1
- update to 1.12.0
- cleaned up and fixed dependencies
- moved Gdata back into main package as it no longer has external deps
- subpackaged more classes with external deps
- added a "full" subpackage to install a full ZF
- new modules: EventManager, Mobile

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.11.12-1
- update to 1.11.12
- fixes ZF2012-01: Local file disclosure via XXE injection in Zend_XmlRpc

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 14 2011 Felix Kaechele <heffer@fedoraproject.org> - 1.11.11-1
- update to 1.11.11
- full changelog http://framework.zend.com/changelog/1.11.11
- spec cleanup

* Thu Aug 04 2011 Felix Kaechele <heffer@fedoraproject.org> - 1.11.10-1
- update to 1.11.10
- full changelog http://framework.zend.com/changelog/1.11.10

* Sat Jul 16 2011 Felix Kaechele <heffer@fedoraproject.org> - 1.11.9-1
- update to 1.11.9
- fixes some nasty bugs
- full changelog http://framework.zend.com/changelog/1.11.9

* Fri Jul 08 2011 Felix Kaechele <heffer@fedoraproject.org> - 1.11.8-1
- update to 1.11.8
- full changelog http://framework.zend.com/changelog/1.11.8
- removed bundled Dojo

* Sun Jun 12 2011 Felix Kaechele <heffer@fedoraproject.org> - 1.11.7-1
- update to 1.11.7
- full changelog http://framework.zend.com/changelog/1.11.7

* Mon May 23 2011 Felix Kaechele <heffer@fedoraproject.org> - 1.11.6-1
- update to 1.11.6
- fixes ZF2011-02: Potential SQL Injection Vector When Using PDO_MySql
- full changelog http://framework.zend.com/changelog/1.11.6

* Fri Mar 04 2011 Felix Kaechele <heffer@fedoraproject.org> - 1.11.4-1
- update to 1.11.4
- over 40 bugs were fixed
- full changelog http://framework.zend.com/changelog/1.11.4

* Wed Feb 09 2011 Felix Kaechele <heffer@fedoraproject.org> - 1.11.3-1
- update to 1.11.3
- full changelog http://framework.zend.com/changelog/1.11.3

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 04 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.11.0-1
- update to 1.11.0
- new component: Cloud
- full changelog http://framework.zend.com/changelog/1.11.0
- release announcement:
  http://devzone.zend.com/article/12724-Zend-Framework-1.11.0-FINAL-Released

* Sun Jul 25 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.10.6-1
- update to 1.10.6 containing over 30 bugfixes

* Sat Jun 12 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.10.5-1
- update to 1.10.5 which contains over 60 bugfixes

* Thu May 13 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.10.4-1
- about 180 bugfixes since 1.10.2 (http://framework.zend.com/changelog/1.10.4)
- fixes ZF2010-07: Potential Security Issues in Bundled Dojo Library

* Wed Mar 03 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.10.2-1
- 1.10.2
- over 50 bugfixes since 1.10.1 (which in turn had over 50 bugfixes)

* Sun Jan 31 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.10-1
- 1.10
- new components: Barcode, Oauth, Markup, Serializer

* Thu Jan 14 2010 Alexander Kahl <akahl@imttechnologies.com> - 1.9.7-1
- update to bugfix / security release 1.9.7 

* Tue Dec 08 2009 Felix Kaechele <felix@fetzig.org> - 1.9.6-2
- insert correct provides/obsoletes for tests subpackage removal

* Mon Nov 30 2009 Felix Kaechele <heffer@fedoraproject.org> - 1.9.6-1
- update to 1.9.6

* Sun Nov 15 2009 Felix Kaechele <felix@fetzig.org> - 1.9.5-1
- update to 1.9.5
- removed test subpackage as it can never comply to font packaging guidelines

* Wed Sep 30 2009 Felix Kaechele <heffer@fedoraproject.org> - 1.9.3-1.PL1
- new upstream version
- new component: Queue
- fixed dangling symlinks
- enabled Db-Adapter-Firebird

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.4-3.PL1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Alexander Kahl <akahl@iconmobile.com> - 1.8.4-2.PL1
- removed Fileinfo dependency
- don't make zf.sh symlink absolute (breaks the script)

* Thu Jul 16 2009 Alexander Kahl <akahl@iconmobile.com> - 1.8.4-1.PL1
- update to 1.8.4 patch 1 (it's about time!)
- Requires php 5.1.4 -> 5.2.4
- list all files explicitly for easier future updates
- incubator no more (Zend_Tool stable now)
- Request now part of Controller
- new components: Application, CodeGenerator, Crypt, Navigation, Reflection,
  Tag
- Soap and Services require php-soap now

* Tue Mar 17 2009 Alexander Kahl <akahl@iconmobile.com> - 1.7.7-2
- bump to catch up with with f10

* Tue Mar 17 2009 Alexander Kahl <akahl@iconmobile.com> - 1.7.7-1
- update to 1.7.7
- PHPUnit dep now >= 3.3.0
- moved Ldap bindings to extra packages (php-ldap dep)
- excluded db adapters with unresolvable deps
- moved mysqli db adapter files to correct package
- support both old and new font deps using conditional

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.7.2-5
- Fix font [Build]Requires yet again to track moving target of naming
  convention.  Fixes broken deps.

* Mon Jan 12 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.7.2-4
- Fix Requires, BuildRequires: bitstream-vera-fonts-{sans,sans-mono,serif}
  fixes broken deps

* Fri Jan  2 2009 Alexander Kahl <akahl@iconmobile.com> - 1.7.2-3
- +BuildRequires: bitstream-vera-fonts
- -Requires: bitstream-vera-fonts

* Fri Jan  2 2009 Alexander Kahl <akahl@iconmobile.com> - 1.7.2-2
- Bug 477440: Use Vera fonts from Fedora's package

* Fri Jan  2 2009 Alexander Kahl <akahl@iconmobile.com> - 1.7.2-1
- update to 1.7.2
- ZendX documentation doesn't need regeneration anymore, removed deps

* Wed Nov 19 2008 Alexander Kahl <akahl@iconmobile.com> - 1.7.0-3
- fix to use internal docbook

* Wed Nov 19 2008 Alexander Kahl <akahl@iconmobile.com> - 1.7.0-2
- bump for rawhide (Zend_Tool activated)

* Tue Nov 18 2008 Alexander Kahl <akahl@iconmobile.com> - 1.7.0-1
- update to 1.7.0

* Wed Nov 12 2008 Alexander Kahl <akahl@iconmobile.com> - 1.6.2-2
- last tag failed, bump

* Wed Nov 12 2008 Alexander Kahl <akahl@iconmobile.com> - 1.6.2-1
- update to 1.6.2

* Tue Sep 16 2008 Alexander Kahl <akahl@iconmobile.com> - 1.6.1-1
- update to 1.6.1

* Sat Sep 13 2008 Alexander Kahl <akahl@iconmobile.com> - 1.6.0-1
- update to 1.6.0 stable (full version)
- create list of invalid executables in %%build for upstream
- new components Captcha, Dojo, Service-ReCaptcha, Wildfire, Zend_Tool
- BuildRequire symlinks to sanitize zf -> zf.sh symlink

* Sat Aug  2 2008 Alexander Kahl <akahl@iconmobile.com> - 1.6.0-0.2.rc1
- added license file to all packages to silence rpmline

* Tue Jul 29 2008 Alexander Kahl <akahl@iconmobile.com> - 1.6.0-0.1.rc1
- update to 1.6.0RC1
- added php-Fileinfo dependency

* Wed Jun 11 2008 Alexander Kahl <akahl@iconmobile.com> - 1.5.2-1
- update to 1.5.2
- new package split
- removed Cache-Backend-Sqlite, Db-Adapter-Db2, Db-Adapter-Firebird,
  Db-Adapter-Oracle
- removed optional php-bitset requirement from Search-Lucene, not available
- removed virtual requires and provides, not necessary anymore

* Mon Mar 17 2008 Alexander Kahl <akahl@iconmobile.com> - 1.5.0-1
- updated for 1.5.0 stable

* Mon Mar 17 2008 Alexander Kahl <akahl@iconmobile.com> - 1.5.0-1.rc3
- new upstream version rc3
- updated for 1.5.0 stable
- new subpackages Ldap and Service-Nirvanix

* Fri Mar  7 2008 Alexander Kahl <akahl@iconmobile.com> - 1.5.0-2.rc1
- added missing dependencies

* Thu Mar  6 2008 Alexander Kahl <akahl@iconmobile.com> - 1.5.0-1.rc1
- new release candidate version 1.5.0
- package all zend components in subpackages

* Wed Dec 12 2007 Alexander Kahl <akahl@iconmobile.com> - 1.0.3-1
- new stable version 1.0.3
- preserve timestamps upon copying
- split up documentation into subpackages
- description BE->AE

* Tue Oct 30 2007 Alexander Kahl <akahl@iconmobile.com> - 1.0.2-1
- initial release
