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

%global pear_name Net_LDAP2

%if 0%{?suse_version}
Name:               php5-pear-Net_LDAP2
%else
Name:               php-pear-Net-LDAP2
%endif
Version:            2.0.12
Release:            1%{?dist}
Summary:            Object oriented interface for searching and manipulating LDAP-entries
Group:              Development/Libraries
License:            LGPLv3
URL:                http://pear.php.net/package/Net_LDAP2
Source0:            http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:          noarch

BuildRequires:      php-pear

Requires(post):     %{__pear}
Requires(postun):   %{__pear}
Requires:           php-pear

Provides:           php-pear(%{pear_name}) = %{version}-%{release}

%description
Net_LDAP2 is the successor of Net_LDAP which is a clone of Perls Net::LDAP
object interface to directory servers. It does contain most of Net::LDAPs
features but has some own too.
With Net_LDAP2 you have:
* A simple object-oriented interface to connections, searches entries and filters.
* Support for tls and ldap v3.
* Simple modification, deletion and creation of ldap entries.
* Support for schema handling.

Net_LDAP2 layers itself on top of PHP's existing ldap extensions.

%prep
%setup -q -c

mv package.xml %{pear_name}-%{version}/%{pear_name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot} docdir

pushd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{pear_name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_phpdir}/.??*

# Install XML package description
%{__mkdir_p} %{buildroot}%{pear_xmldir}
%{__install} -pm 644 %{pear_name}.xml %{buildroot}%{pear_xmldir}

popd

# For troubleshooting macros:

echo "pear_metadir: '%{pear_metadir}'"

%check
# Sanity check
lst=$(find %{buildroot}%{pear_phpdir} -exec grep -q %{buildroot} {} \; -print)
[ ! -z "$lst" ] && echo "Reference to BUILDROOT in $lst" && exit 1;

%clean
rm -rf %{buildroot}

%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{pear_name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi

%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%dir %{pear_phpdir}/Net
%{pear_phpdir}/Net/LDAP2
%{pear_phpdir}/Net/LDAP2.php
%{pear_testdir}/%{pear_name}
%if 0%{?suse_version}
%dir %{pear_xmldir}
%endif
%{pear_xmldir}/%{pear_name}.xml
%if 0%{?rhel} > 6 || 0%{?fedora} > 18
%{pear_metadir}/.registry/net_ldap2.reg
%exclude %{pear_metadir}
%endif

%changelog
* Sat Jun 05 2010 Christoph Wickert <wickert@kolabsys.com> - 2.0.9-3
- Adjust requirements for php-channel(pear.horde.org)

* Sun May  9 2010 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.0.9-2
- Package for Fedora/EPEL

