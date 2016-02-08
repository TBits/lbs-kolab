%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%{!?pear_docdir: %global pear_docdir %(%{__pear} config-get doc_dir)}
%{!?pear_phpdir: %global pear_phpdir %(%{__pear} config-get php_dir)}
%{!?pear_testdir: %global pear_testdir %(%{__pear} config-get test_dir)}
%{!?pear_xmldir: %global pear_xmldir /var/lib/pear/pkgxml}

%global          pear_name Net_IDNA2

Summary:         PHP library for punycode encoding and decoding

%if 0%{?suse_version}
Name:            php5-pear-Net-IDNA2
%else
Name:            php-pear-Net-IDNA2
%endif

Version:         0.1.1
Release:         10%{?dist}
License:         LGPLv2+
Group:           Development/Libraries
URL:             http://pear.php.net/package/Net_IDNA2/
Source0:         http://download.pear.php.net/package/Net_IDNA2-%{version}.tgz
BuildArch:       noarch
%if 0%{?suse_version}
BuildRequires:   php-pear
%else
BuildRequires:   php-pear(PEAR) >= 1.9.1
%endif

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:        php-common >= 5.3.0
Requires:        php-pear(PEAR)
Requires(post):  %{__pear}
Requires(preun): %{__pear}
Provides:        php-pear(%{pear_name}) = %{version}

%description
This package helps you to encode and decode punycode strings easily in
PHP.

%prep
%setup -q -c
# Create a "localized" php.ini to avoid build warning
if [ -f /etc/php.ini ]; then
    cp /etc/php.ini .
fi

echo "date.timezone=UTC" >> php.ini
pushd %{pear_name}-%{version}
mv ../package.xml %{name}.xml
popd

%build
# Nothing to build

%install
rm -rf %{buildroot}
pushd %{pear_name}-%{version}
PHPRC=../php.ini %{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Move documentation
mkdir -p docdir
mv %{buildroot}%{pear_docdir}/%{pear_name}/docs ../docdir
rm -rf %{buildroot}%{pear_docdir}

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
install -D -p -m 0644 %{name}.xml %{buildroot}%{pear_xmldir}/%{name}.xml

%clean
rm -rf %{buildroot}

%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null ||:

%postun
if [ "$1" -eq "0" ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null ||:
fi

%files
%defattr(-, root, root, -)
%doc docdir/*
%dir %{pear_phpdir}/Net/
%{pear_phpdir}/Net/IDNA2
%{pear_phpdir}/Net/IDNA2.php
%{pear_testdir}/%{pear_name}
%if 0%{?suse_version}
%dir %{pear_xmldir}
%endif
%{pear_xmldir}/%{name}.xml

%changelog
* Wed Jun 25 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.1.1-11
- Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 20 2013 Terje Rosten <terje.rosten@ntnu.no> - 0.1.1-8
- Fix build

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 0.1.1-6
- rebuilt for new pear_testdir

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Feb 19 2011 Terje Rosten <terje.rosten@ntnu.no> - 0.1.1-3
- Own Net dir

* Sat Feb 12 2011 Terje Rosten <terje.rosten@ntnu.no> - 0.1.1-2
- add fedoraism
- fix license

* Sat Jan 22 2011 Adam Williamson <awilliamson@mandriva.org> - 0.1.1-1
- revision: 632388
- add source
- fix source extension
- imported package php-pear-Net_IDNA2


