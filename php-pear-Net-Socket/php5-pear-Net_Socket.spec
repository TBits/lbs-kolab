#
# spec file for package php5-pear-Net_Socket
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


Name:           php5-pear-Net_Socket
%define pear_name  Net_Socket
%define pear_sname net_socket
Summary:        Network Socket Interface
License:        PHP-3.01
Group:          Productivity/Networking/Web/Servers
Version:        1.0.10
Release:        0
BuildArch:      noarch
Url:            http://pear.php.net/package/%{pear_name}
Source:         %{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  php >= 4.0.0
%if 0%{?sles_version} == 10
BuildRequires:  php-macros
%else
BuildRequires:  php-devel >= 4.0.0
%endif
BuildRequires:  php-pear >= 1.4.0
Requires:       php >= 4.0.0
Requires:       php-pear >= 1.4.0

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
Net_Socket is a class interface to TCP sockets. It provides blocking
and non-blocking operation, with different reading and writing modes
(byte-wise, block-wise, line-wise and special formats like network
byte-order ip addresses).

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

%changelog
