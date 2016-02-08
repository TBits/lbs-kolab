#
# spec file for package php5-pear-DB
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           php5-pear-DB
%define pear_name  DB
%define pear_sname db
Summary:        Database Abstraction Layer
License:        PHP-3.01
Group:          Productivity/Networking/Web/Servers
Version:        1.7.14
Release:        0
BuildArch:      noarch
Url:            http://pear.php.net/package/%{pear_name}
Source:         http://download.pear.php.net/package/DB-%{version}.tgz
Source1:        %{pear_name}.rpmlintrc

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  php >= 4.2.0
%if 0%{?sles_version} == 10
BuildRequires:  php-macros
%else
BuildRequires:  php-devel >= 4.2.0
%endif
BuildRequires:  php-pear >= 1.4.0
Requires:       php >= 4.2.0
Requires:       php-pear >= 1.4.0

Provides:       pear-%{pear_name}
Provides:       pear-%{pear_sname} = %{version}
Provides:       php-pear-%{pear_name}
Provides:       php-pear(%{pear_name}) = %{version}
Provides:       php-pear-%{pear_sname} = %{version}
Provides:       php5-pear-%{pear_sname} = %{version}
Obsoletes:      pear-%{pear_sname} < %{version}
Obsoletes:      php-pear-%{pear_sname} < %{version}
Obsoletes:      php5-pear-%{pear_sname} < %{version}

%description
DB is a database abstraction layer providing:
* an OO-style query API
* portability features that make programs written for one DBMS work with other DBMS's
* a DSN (data source name) format for specifying database servers
* prepare/execute (bind) emulation for databases that don't support it natively
* a result object for each query response
* portable error codes
* sequence emulation
* sequential and non-sequential row fetching as well as bulk fetching
* formats fetched rows as associative arrays, ordered arrays or objects
* row limit support
* transactions support
* table information interface
* DocBook and phpDocumentor API documentation

DB layers itself on top of PHP's existing database extensions.

Drivers for the following extensions pass the complete test suite and provide
interchangeability when all of DB's portability options are enabled:

  fbsql, ibase, informix, msql, mssql,
  mysql, mysqli, oci8, odbc, pgsql,
  sqlite and sybase.

There is also a driver for the dbase extension, but it can't be used
interchangeably because dbase doesn't support many standard DBMS features.

DB is compatible with both PHP 4 and PHP 5.

%prep
%setup -c

%build

%install
%{__mv} package*.xml %{pear_name}-%{version}
cd %{pear_name}-%{version}
PHP_PEAR_PHP_BIN="$(which php) -d memory_limit=50m"
%{__pear} -v \
        -d doc_dir=/doc \
        -d bin_dir=%{_bindir} \
        -d data_dir=%{php_peardir}/data \
        install --offline --nodeps -R "%{buildroot}" package.xml

%{__install} -D -m 0644 package.xml %{buildroot}%{php_pearxmldir}/%{pear_name}.xml

%{__rm} -rf %{buildroot}/{doc,tmp}
%{__rm} -rf "%{buildroot}"/%{php_peardir}/.{filemap,lock,registry,channels,depdb,depdblock}

# fix for brp-check-buildroot
%{__sed} -i -e "s@%{buildroot}@@g" %{buildroot}%{php_peardir}/test/%{pear_name}/tests/driver/setup.inc
%{__sed} -i -e "s@%{buildroot}@@g" %{buildroot}%{php_peardir}/test/%{pear_name}/tests/include.inc
cd ..

%php_pear_gen_filelist

%post
# on `rpm -ivh` PARAM is 1
# on `rpm -Uvh` PARAM is 2
if [ "$1" = "1" ]; then
  %{__pear} install --nodeps --soft --force --register-only %{php_pearxmldir}/%{pear_name}.xml
fi
if [ "$1" = "2" ]; then
  %{__pear} upgrade --offline --register-only %{php_pearxmldir}/%{pear_name}.xml
fi

%postun
# on `rpm -e` PARAM is 0
if [ "$1" = "0" ]; then
  %{__pear} uninstall --nodeps --ignore-errors --register-only pear.php.net/%{pear_name}
fi

%clean
%{__rm} -rf %{buildroot}

%files -f %{name}.files
%defattr(-, root, root)
%doc %{pear_name}-%{version}/doc/*

%changelog
