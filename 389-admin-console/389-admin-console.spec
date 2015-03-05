#
# spec file for package 389-admin-console
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


Name:           389-admin-console
Version:        1.1.8
Release:        0
Summary:        389 Admin Server Management Console

Group:          Productivity/Networking/LDAP/Utilities
License:        GPL-2.0
Url:            http://port389.org
Source:         http://port389.org/sources/%{name}-%{version}.tar.bz2

BuildArch:      noarch
BuildRequires:  ant >= 1.6.2
BuildRequires:  idm-console-framework >= 1.1
BuildRequires:  ldapjdk
BuildRequires:  java-devel >= 1.6.0
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

#Requires:       389-admin
Requires:       389-console

%define major_version 1.1
%define shortname 389-admin
%define pkgname dirsrv

%description
A Java based remote management console used for Managing 389
Admin Server.  Requires the 389 Console to load and run the
jar files.


%package          doc
Summary:          Web docs for 389 Admin Server Management Console
Group:            Documentation/Man
Requires:         %{name} = %{version}-%{release}

%description      doc
389-admni-console is a Java based remote management console used for Managing 389
Admin Server.  Requires the 389 Console to load and run the jar files.

This package contains web docs for 389 Admin Server Management Console


%prep
%setup -q

%build
%{ant} \
    -Dconsole.location=%{_javadir} \
    -Dbuilt.dir=`pwd`/built

%install
export NO_BRP_CHECK_BYTECODE_VERSION=true
install -d %{buildroot}%{_datadir}/%{pkgname}/html/java
install -m644 built/package/%{shortname}* %{buildroot}%{_datadir}/%{pkgname}/html/java
install -d %{buildroot}%{_datadir}/%{pkgname}/manual/en/admin/help
install -m644 help/en/*.html %{buildroot}%{_datadir}/%{pkgname}/manual/en/admin
install -m644 help/en/tokens.map %{buildroot}%{_datadir}/%{pkgname}/manual/en/admin
install -m644 help/en/help/*.html %{buildroot}%{_datadir}/%{pkgname}/manual/en/admin/help

# create symlinks
pushd %{buildroot}%{_datadir}/%{pkgname}/html/java
ln -s %{shortname}-%{version}.jar %{shortname}-%{major_version}.jar
ln -s %{shortname}-%{version}.jar %{shortname}.jar
ln -s %{shortname}-%{version}_en.jar %{shortname}-%{major_version}_en.jar
ln -s %{shortname}-%{version}_en.jar %{shortname}_en.jar
popd

%files
%defattr(-,root,root)
%doc LICENSE
%dir %{_datadir}/%{pkgname}
%dir %{_datadir}/%{pkgname}/html
%dir %{_datadir}/%{pkgname}/html/java
%{_datadir}/%{pkgname}/html/java/%{shortname}-%{version}.jar
%{_datadir}/%{pkgname}/html/java/%{shortname}-%{major_version}.jar
%{_datadir}/%{pkgname}/html/java/%{shortname}.jar
%{_datadir}/%{pkgname}/html/java/%{shortname}-%{version}_en.jar
%{_datadir}/%{pkgname}/html/java/%{shortname}-%{major_version}_en.jar
%{_datadir}/%{pkgname}/html/java/%{shortname}_en.jar

%files doc
%defattr(-,root,root)
%dir %{_datadir}/%{pkgname}
%dir %{_datadir}/%{pkgname}/manual
%dir %{_datadir}/%{pkgname}/manual/en
%dir %{_datadir}/%{pkgname}/manual/en/admin
%dir %{_datadir}/%{pkgname}/manual/en/admin/help
%doc %{_datadir}/%{pkgname}/manual/en/admin/tokens.map
%doc %{_datadir}/%{pkgname}/manual/en/admin/*.html
%doc %{_datadir}/%{pkgname}/manual/en/admin/help/*.html

%changelog
