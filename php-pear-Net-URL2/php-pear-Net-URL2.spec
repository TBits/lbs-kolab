# spec file for php-pear-Net-URL2
#
# Copyright (c) 2009-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:         %{expand: %%global __pear %{_bindir}/pear}}

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

%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name   Net_URL2
%global with_tests  %{?_with_tests:1}%{!?_with_tests:0}

Name:           php-pear-Net-URL2
Version:        2.1.1
Release:        1%{?dist}
Summary:        Class for parsing and handling URL

Group:          Development/Libraries
License:        BSD
URL:            http://pear.php.net/package/Net_URL2
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear
%if %{with_tests}
BuildRequires:  php-phpunit-PHPUnit
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
# From phpcompatinfo report for 2.1.1
Requires:       php-pcre

Provides:       php-pear(%{pear_name}) = %{version}
Provides:       php-composer(pear/net_url2) = %{version}


%description
Provides parsing of URLs into their constituent parts (scheme, host, path
etc.), URL generation, and resolving of relative URLs.


%prep
%setup -q -c

cd %{pear_name}-%{version}
# Package is V2
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*
%{__rm} -rf %{buildroot}/usr/share/php5/PEAR/.{filemap,lock,registry,channels,depdb,depdblock}

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%check
%if %{with_tests}
# test suite cannot run in mock (use network)
# Version 2.1.1 : OK (113 tests, 270 assertions)
cd %{buildroot}%{pear_testdir}/%{pear_name}/tests
phpunit \
   -d date.timezone=UTC \
   --include-path=%{buildroot}%{pear_phpdir} \
   AllTests.php
%else
echo 'Test suite disabled (missing "--with tests" option)'
%endif


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.php.net/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Net
%{pear_testdir}/%{pear_name}
%{pear_xmldir}

%changelog
* Sun Dec 28 2014 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- Update to 2.1.1

* Mon Oct 27 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0 (no change, for semver)

* Sat Oct 18 2014 Remi Collet <remi@fedoraproject.org> - 2.0.11-1
- Update to 2.0.11

* Fri Oct 10 2014 Remi Collet <remi@fedoraproject.org> - 2.0.10-1
- Update to 2.0.10 (stable) - no change
- provide php-composer(pear/net_url2)

* Thu Oct  9 2014 Remi Collet <remi@fedoraproject.org> - 2.0.9-1
- Update to 2.0.9 (stable)

* Wed Oct  8 2014 Remi Collet <remi@fedoraproject.org> - 2.0.8-1
- Update to 2.0.8 (stable)

* Mon Sep  8 2014 Remi Collet <remi@fedoraproject.org> - 2.0.7-1
- Update to 2.0.7 (stable)

* Mon Jun 23 2014 Remi Collet <remi@fedoraproject.org> - 2.0.6-1
- Update to 2.0.6 (stable)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan  2 2014 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- Update to 2.0.5 (stable)

* Tue Dec 31 2013 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4 (stable)

* Mon Dec 30 2013 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3 (stable)

* Sat Dec 28 2013 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2 (stable)

* Wed Dec 25 2013 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1 (stable)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 19 2013 Remi Collet <remi@fedoraproject.org> - 2.0.0-6
- fix metadata location

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-4
- rebuilt for new pear_testdir

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 22 2011 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Version 2.0.0 (stable) - API 2.0.0 (stable)
- add tests option to run tests during rpmbuild

* Mon Apr 18 2011 Remi Collet <Fedora@FamilleCollet.com> 0.3.1-4
- doc in /usr/share/doc/pear
- set date.timezone during build

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat May 22 2010 Remi Collet <Fedora@FamilleCollet.com> 0.3.1-2
- spec cleanup

* Sun Jan 24 2010 Remi Collet <Fedora@FamilleCollet.com> 0.3.1-1
- update to 0.3.1

* Wed Nov 11 2009 Remi Collet <Fedora@FamilleCollet.com> 0.3.0-1
- initial RPM

