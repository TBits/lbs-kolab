#
# spec file for package php5-pear-Net_SMTP
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
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


Name:           php5-pear-Net_SMTP
%define pear_name  Net_SMTP
%define pear_sname net_smtp
Summary:        An implementation of the SMTP protocol
License:        PHP-3.01
Group:          Productivity/Networking/Web/Servers
Version:        1.6.1
Release:        0
BuildArch:      noarch
Url:            http://pear.php.net/package/%{pear_name}
Source:         %{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%if 0%{?sles_version} == 11
BuildRequires:  php53-devel
%else
BuildRequires:  php-macros
%endif
BuildRequires:  php >= 4.0.5
BuildRequires:  php-pear
Requires:       php >= 4.0.5
Requires:       php-pear
Requires:       php-pear-Net_Socket >= 1.0.7
Suggests:       php-pear-Auth_SASL
#
Provides:       pear-%{pear_name}
Provides:       php-pear-%{pear_name}
Provides:       php-pear(%{pear_name}) = %{version}
# Fix for renaming (package convention)
Provides:       pear-%{pear_sname} = %{version}
Provides:       php-pear-%{pear_sname} = %{version}
Provides:       php5-pear-%{pear_sname} = %{version}
Obsoletes:      pear-%{pear_sname} < %{version}
Obsoletes:      php-pear-%{pear_sname} < %{version}
Obsoletes:      php5-pear-%{pear_sname} < %{version}

%description
Provides an implementation of the SMTP protocol using PEAR's Net_Socket class.

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
%{__rm} -rf %{buildroot}%{php_peardir}/.{filemap,lock,registry,channels,depdb,depdblock}

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
%doc %{pear_name}-%{version}/docs/*
%doc %{pear_name}-%{version}/examples

%changelog
