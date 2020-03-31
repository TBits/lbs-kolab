# Spec file for php-sabre-http
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    6b06c03376219b3d608e1f878514ec105ed1b577
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     fruux
%global gh_project   sabre-http
#global prever       alpha6
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-%{gh_project}
Summary:        Library for dealing with http requests and responses
Version:        3.0.5
Release:        3.33%{?dist}.kolab_16

URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?prever}.tar.gz
License:        BSD
Group:          Development/Libraries

BuildArch:      noarch
%if %{with_tests}
%if 0%{?suse_version}
BuildRequires:  php5 > 5.4
%else
BuildRequires:  php(language) > 5.4
%endif
BuildRequires:  php-phpunit-PHPUnit
BuildRequires:  php-composer(sabre/event) >= 1.0.0
BuildRequires:  php-composer(sabre/event) <  3
%endif

# From composer.json
#        "php"          : ">=5.4",
#        "ext-mbstring" : "*",
#        "sabre/event"  : ">=1.0.0,<3.0.0"
%if 0%{?suse_version}
Requires:       php5 > 5.4
%else
Requires:       php(language) > 5.4
%endif
Requires:       php-curl
Requires:       php-mbstring
Requires:       php-composer(sabre/event) >= 1.0.0
Requires:       php-composer(sabre/event) <  3
# From phpcompatinfo report for version 2.0.4
Requires:       php-ctype
Requires:       php-date
Requires:       php-pcre
Requires:       php-spl
Requires:       php-xml
# Was split from php-sabre-dav in version 1.9
Conflicts:      php-sabre-dav < 1.9

Provides:       php-composer(sabre/http) = %{version}


%description
This library provides a toolkit to make working with the HTTP protocol easier.

Most PHP scripts run within a HTTP request but accessing information about
the HTTP request is cumbersome at least, mainly do to superglobals and the
CGI standard.

There's bad practices, inconsistencies and confusion.
This library is effectively a wrapper around the following PHP constructs:

For Input:
    $_GET
    $_POST
    $_SERVER
    php://input or $HTTP_RAW_POST_DATA.

For output:
    php://output or echo.
    header()

What this library provides, is a Request object, and a Response object.
The objects are extendable and easily mockable.


%prep
##%%setup -q -n %{gh_project}-%{gh_commit}
%setup -q -n %{gh_project}-%{version}

: Create trivial PSR0 autoloader
cat <<EOF | tee psr0.php
<?php
spl_autoload_register(function (\$class) {
    \$file = str_replace('\\\\', '/', \$class).'.php';
    @include \$file;
});
EOF


%build
# nothing to build


%install
# Install as a PSR-0 library
mkdir -p %{buildroot}%{_datadir}/php/Sabre/HTTP
cp -pr lib/* %{buildroot}%{_datadir}/php/Sabre/HTTP/.


%check
%if %{with_tests}
: Run upstream test suite against installed library
cd tests
phpunit \
  --bootstrap=../psr0.php \
  --include-path=%{buildroot}%{_datadir}/php \
  -d date.timezone=UTC
%else
: Skip upstream test suite
%endif


%files
%doc ChangeLog.md composer.json LICENSE README.md
%{_datadir}/php/Sabre/HTTP


%changelog
* Wed Jul 16 2014 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- update to 2.0.4
- composer dependencies

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May  6 2014 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- update to 2.0.3

* Tue Feb 11 2014 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- update to 2.0.2

* Sat Jan 11 2014 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1

* Tue Jan  7 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.2.alpha6
- update to 2.0.0alpha6
- add explicit conflicts with php-sabre-dav < 1.9

* Tue Dec 31 2013 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.alpha5
- Initial packaging
