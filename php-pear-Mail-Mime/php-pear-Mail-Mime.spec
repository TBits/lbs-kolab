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

%global pear_name Mail_Mime

%if 0%{?suse_version}
Name:               php5-pear-Mail_Mime
%else
Name:               php-pear-Mail-Mime
%endif

Summary:            Mail_Mime provides classes to create mime messages
License:            BSD-3-Clause
Group:              Productivity/Networking/Web/Servers
Version:            1.8.7
Release:            1%{?dist}
BuildArch:          noarch
Url:                http://pear.php.net/package/%{pear_name}
Source:             %{pear_name}-%{version}.tgz

BuildRoot:          %{_tmppath}/%{name}-%{version}-build
BuildRequires:      php-pear

Requires(post):     %{__pear}
Requires(postun):   %{__pear}
Requires:           php-pear

Provides:           php-pear(%{pear_name}) = %{version}-%{release}

%description
Mail_Mime provides classes to deal with the creation and manipulation of mime messages.
It allows people to create Email messages consisting of:
* Text Parts
* HTML Parts
* Inline HTML Images
* Attachments
* Attached messages

Starting with version 1.4.0, it also allows non US-ASCII chars in filenames,
 subjects, recipients, etc, etc.

%prep
%setup -q -c

cd %{pear_name}-%{version}
# package.xml is V2
mv ../package.xml %{name}.xml

%build

%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_phpdir}/.??*

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

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%doc %{pear_docdir}/%{pear_name}
%if 0%{?suse_version}
%dir %{pear_xmldir}
%endif
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Mail
%{pear_testdir}/%{pear_name}

%changelog
