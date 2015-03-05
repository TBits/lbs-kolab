#
# spec file for package php5-pear-MDB2
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


Name:           php5-pear-MDB2
%define pear_name  MDB2
%define pear_sname mdb2
Summary:        Database abstraction layer
License:        BSD-3-Clause
Group:          Productivity/Networking/Web/Servers
Version:        2.5.0b5
Release:        0
BuildArch:      noarch
Url:            http://pear.php.net/package/%{pear_name}
Source:         %{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  php >= 5.2.0
%if 0%{?sles_version} == 10
BuildRequires:  php-macros
%else
BuildRequires:  php-devel >= 5.2.0
%endif
BuildRequires:  php-pear >= 1.9.1
Requires:       php >= 5.2.0
Requires:       php-pear >= 1.9.1

Provides:       php-pear-%{pear_name} pear-%{pear_name}
# Fix for renaming (package convention)
Provides:       php5-pear-%{pear_sname} = %{version}
Provides:       php-pear-%{pear_sname} = %{version}
Provides:       php-pear(%{pear_name}) = %{version}
Provides:       pear-%{pear_sname} = %{version}
Obsoletes:      php5-pear-%{pear_sname} < %{version}
Obsoletes:      php-pear-%{pear_sname} < %{version}
Obsoletes:      pear-%{pear_sname} < %{version}

%description
PEAR MDB2 is a merge of the PEAR DB and Metabase php database abstraction layers.

It provides a common API for all supported RDBMS. The main difference to most
other DB abstraction packages is that MDB2 goes much further to ensure
portability. MDB2 provides most of its many features optionally that
can be used to construct portable SQL statements:
* Object-Oriented API
* A DSN (data source name) or array format for specifying database servers
* Datatype abstraction and on demand datatype conversion
* Various optional fetch modes to fix portability issues
* Portable error codes
* Sequential and non sequential row fetching as well as bulk fetching
* Ability to make buffered and unbuffered queries
* Ordered array and associative array for the fetched rows
* Prepare/execute (bind) named and unnamed placeholder emulation
* Sequence/autoincrement emulation
* Replace emulation
* Limited sub select emulation
* Row limit emulation
* Transactions/savepoint support
* Large Object support
* Index/Unique Key/Primary Key support
* Pattern matching abstraction
* Module framework to load advanced functionality on demand
* Ability to read the information schema
* RDBMS management methods (creating, dropping, altering)
* Reverse engineering schemas from an existing database
* SQL function call abstraction
* Full integration into the PEAR Framework
* PHPDoc API documentation

%prep
%setup -c

# patch autoload.inc to not include buildroot
sed -i -e '17s/@php_dir@/\/usr\/share\/php5\/PEAR/' MDB2-2.5.0b5/tests/autoload.inc
sed -i -e '21s/@php_dir@/\/usr\/share\/php5\/PEAR/' MDB2-2.5.0b5/tests/autoload.inc

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
%{__rm} -rf %{buildroot}%{php_peardir}/.{filemap,lock,registry,channels,depdb,depdblock}
# remove data, LICENSE to docdir
%{__rm} -rf $RPM_BUILD_ROOT/%{php_peardir}/data

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
%doc %{pear_name}-%{version}/LICENSE
%doc %{pear_name}-%{version}/docs/*

%changelog
