#
# spec file for package 389-console
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
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


Name:           389-console
Version:        1.1.7
Release:        0
Summary:        389 Management Console

Group:          Productivity/Networking/LDAP/Utilities
License:        LGPL-2.0
Url:            http://port389.org
Source:         http://port389.org/sources/%{name}-%{version}.tar.bz2

BuildArch:      noarch
BuildRequires:  ant >= 1.6.2
BuildRequires:  ldapjdk
BuildRequires:  mozilla-jss >=  4.2
BuildRequires:  idm-console-framework >= 1.1
BuildRequires:  java-devel >= 1.6.0
BuildRoot: %{_tmppath}/%{name}-%{version}-build

Requires:       idm-console-framework >= 1.1
Requires:       java >= 1.6.0


%define major_version 1.1

%description
A Java based remote management console used for managing 389
Administration Server and 389 Directory Server.

%prep
%setup -q
                                                                                
%build
%{ant} \
    -Dbuilt.dir=`pwd`/built \
    -Djss.local.location=%{_libdir}/java

# add -Dlib.dir and -Dneed_libdir on those platforms where
# jss is installed in a non-standard location
# -Dneed_libdir=yes

%install
install -d %{buildroot}%{_javadir}
install -m644 built/*.jar %{buildroot}%{_javadir}
install -d %{buildroot}%{_bindir}
install -m755 built/%{name} %{buildroot}/%{_bindir}

# create symlinks
pushd %{buildroot}%{_javadir}
ln -s %{name}-%{version}_en.jar %{name}-%{major_version}_en.jar
ln -s %{name}-%{version}_en.jar %{name}_en.jar
popd

%files
%defattr(-,root,root)
%doc LICENSE
%{_javadir}/%{name}-%{version}_en.jar
%{_javadir}/%{name}-%{major_version}_en.jar
%{_javadir}/%{name}_en.jar
%{_bindir}/%{name}

%changelog
