# remirepo/fedora spec file for php-pear-Net-LDAP2
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name Net_LDAP2

# Needed for openSUSE
%if 0%{?suse_version}
%{!?pear_cfgdir:    %global pear_cfgdir %(%{__pear} config-get cfg_dir  2> /dev/null || echo undefined)}
%{!?pear_datadir:   %global pear_datadir %(%{__pear} config-get data_dir 2> /dev/null || echo undefined)}
%{!?pear_docdir:    %global pear_docdir %(%{__pear} config-get doc_dir  2> /dev/null || echo undefined)}
%{!?pear_metadir:   %global pear_metadir %(%{__pear} config-get metadata_dir 2> /dev/null || echo undefined)}
%{!?pear_phpdir:    %global pear_phpdir %(%{__pear} config-get php_dir  2> /dev/null || echo undefined)}
%{!?pear_testdir:   %global pear_testdir %(%{__pear} config-get test_dir 2> /dev/null || echo undefined)}
%{!?pear_wwwdir:    %global pear_wwwdir %(%{__pear} config-get www_dir  2> /dev/null || echo undefined)}
%{!?pear_xmldir:    %global pear_xmldir %{_localstatedir}/lib/pear/pkgxml}
%endif

# Test suite requires a LDAP server, so are not run during build

%if 0%{?suse_version}
Name:               php5-pear-Net_LDAP2
%else
Name:               php-pear-Net-LDAP2
%endif
Version:        2.2.0
Release:        2%{?dist}
Summary:        Object oriented interface for searching and manipulating LDAP-entries

# LGPL doesn't require license file, but ask for it
# https://pear.php.net/bugs/bug.php?id=20504 - please include License file
License:        LGPLv3
URL:            http://pear.php.net/package/%{pear_name}
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz

Patch1: lower-min-required-pear-version.patch

BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.9.4

Requires(post): %{__pear}
Requires(postun): %{__pear}
# From package.xml
Requires:       php(language)  >= 5.4
Requires:       php-pear(PEAR) >= 1.9.4
Requires:       php-ldap
# From phpcompatinfo report
Requires:       php-date
Requires:       php-pcre
Requires:       php-spl

Provides:       php-pear(%{pear_name}) = %{version}
Provides:       php-composer(pear/net_ldap2) = %{version}


%description
Net_LDAP2 is the successor of Net_LDAP (which is a clone of Perls Net::LDAP)
object interface to directory servers. It does contain most of Net::LDAPs
features but has some own too.

With Net_LDAP2 you have:
* A simple object-oriented interface to connections,
  searches entries and filters.
* Support for TLS and LDAP v3.
* Simple modification, deletion and creation of LDAP entries.
* Support for schema handling.

Net_LDAP2 layers itself on top of PHP's existing ldap extensions.


%prep
%setup -q -c
%patch1 -p1
cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.php.net/%{pear_name} >/dev/null || :
fi


%files
%doc %{pear_docdir}/%{pear_name}
%if 0%{?suse_version}
%dir %{pear_xmldir}
%endif
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Net
%{pear_testdir}/%{pear_name}


%changelog
* Sat Oct 05 2019 Christoph Erhardt <kolab@sicherha.de> - 2.2.0-2
- Package for Kolab
- Fix the build on CentOS/RHEL 7

* Sat Oct 31 2015 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0
- provide php-composer(pear/net_ldap2)
- raise dependency on PEAR 1.10.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Feb 22 2015 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Version 2.1.0 (stable), API 2.0.0 (stable)
- Initial package
