#
# spec file for package php5-pear-Mail_mimeDecode
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


Name:           php5-pear-Mail_mimeDecode
%define pear_name  Mail_mimeDecode
%define pear_sname mail_mimedecode
Summary:        Decode mime messages
License:        BSD-3-Clause
Group:          Productivity/Networking/Web/Servers
Version:        1.5.5
Release:        0
BuildArch:      noarch
Url:            http://pear.php.net/package/%{pear_name}
Source:         %{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  php >= 4.3
%if 0%{?sles_version} == 10
BuildRequires:  php-macros
%else
BuildRequires:  php-devel >= 4.3
%endif
BuildRequires:  php-pear >= 1.6.0
Requires:       php >= 4.3
Requires:       php-pear >= 1.6.0
Requires:       php-pear(Mail_Mime) >= 1.4.0

Provides:       php-pear-%{pear_name} pear-%{pear_name}
# Fix for renaming (package convention)
Provides:       php5-pear-%{pear_sname} = %{version}
Provides:       php-pear(%{pear_name}) = %{version}
Provides:       pear-%{pear_sname} = %{version}
Obsoletes:      php5-pear-%{pear_sname} < %{version}
Obsoletes:      php-pear-%{pear_sname} < %{version}
Obsoletes:      pear-%{pear_sname} < %{version}

%description
Provides a class to deal with the decoding and interpreting of mime messages.
This package used to be part of the Mail_Mime package, but has been split off.

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
