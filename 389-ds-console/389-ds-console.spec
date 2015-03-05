#
# spec file for package 389-ds-console
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


Name:           389-ds-console
Version:        1.2.7
Release:        0
Summary:        389 Directory Server Management Console

Group:          Productivity/Networking/LDAP/Utilities
License:        GPL-2.0
Url:            http://port389.org
Source:         http://port389.org/sources/%{name}-%{version}.tar.bz2

BuildArch:      noarch
BuildRequires:  ant >= 1.6.2
BuildRequires:  idm-console-framework >= 1.1
BuildRequires:  java-devel >= 1.6.0
BuildRequires:  ldapjdk
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

Requires:       389-admin

%define major_version 1.2
%define shortname 389-ds
%define pkgname   dirsrv

%description
A Java based remote management console used for managing 389
Directory Server. Requires the 389 Console installed (on a client)
to load and run the jar files from an 389-admin server.

This package has to be installed on the adminstration server.


%package        doc
Summary:        Web docs for 389 Directory Server Management Console
Group:          Documentation/Man
Requires:       %{name} = %{version}-%{release}

%description      doc
The 389 Console is a Java based remote management console used for managing 389
Directory Server.

This package contains Web docs for 389 Directory Server Management Console.


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
install -d %{buildroot}%{_datadir}/%{pkgname}/manual/en/slapd/help
install -m644 help/en/*.html %{buildroot}%{_datadir}/%{pkgname}/manual/en/slapd
install -m644 help/en/tokens.map %{buildroot}%{_datadir}/%{pkgname}/manual/en/slapd
install -m644 help/en/help/*.html %{buildroot}%{_datadir}/%{pkgname}/manual/en/slapd/help

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
%dir %{_datadir}/%{pkgname}/manual/en/slapd
%dir %{_datadir}/%{pkgname}/manual/en/slapd/help
%doc %{_datadir}/%{pkgname}/manual/en/slapd/tokens.map
%doc %{_datadir}/%{pkgname}/manual/en/slapd/*.html
%doc %{_datadir}/%{pkgname}/manual/en/slapd/help/*.html
                                                                                
%changelog
