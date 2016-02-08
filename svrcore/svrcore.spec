#
# spec file for package svrcore
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
# Copyright (c) 2009-2011 Wolfgang Rosenauer
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

# norootforbuild


Name:           svrcore
BuildRequires:  mozilla-nss-devel pkgconfig
Summary:        Secure PIN handling using NSS crypto
Version:        4.0.4
Release:        1
License:        MPL-1.1 or GPL-2.0+ or LGPL-2.1+
Url:            http://www.mozilla.org/projects/security/pki/
Group:          System/Libraries
Source0:        ftp://ftp.mozilla.org/pub/mozilla.org/directory/svrcore/releases/%{version}/src/svrcore-%{version}.tar.bz2
Source1:        baselibs.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%define libpackage libsvrcore0

%description
svrcore provides applications with several ways to handle secure PIN storage
e.g. in an application that must be restarted, but needs the PIN to unlock
the private key and other crypto material, without user intervention.  svrcore
uses the facilities provided by NSS.


%package -n %{libpackage}

Summary:        Secure PIN handling using NSS crypto
License:        MPL-1.1 or GPL-2.0+ or LGPL-2.1+
Group:          System/Libraries

%description -n libsvrcore0
svrcore provides applications with several ways to handle secure PIN storage
e.g. in an application that must be restarted, but needs the PIN to unlock
the private key and other crypto material, without user intervention.  svrcore
uses the facilities provided by NSS.


%package devel
Summary:        Development files for secure PIN handling using NSS crypto
License:        MPL-1.1 or GPL-2.0+ or LGPL-2.1+
Group:          Development/Libraries/Other
Requires:       %{libpackage} = %{version}-%{release}
Requires:       pkgconfig mozilla-nspr-devel mozilla-nss-devel

%description devel
svrcore provides applications with several ways to handle secure PIN storage
e.g. in an application that must be restarted, but needs the PIN to unlock
the private key and other crypto material, without user intervention.  svrcore
uses the facilities provided by NSS.

This package contains header files and symlinks to develop programs which will
use the libsvrcore library.  You should install this package if you need to
develop programs which will use the svrcore library.

%prep
%setup -q

%build
%configure
%__make

%install
%makeinstall
rm -f $RPM_BUILD_ROOT%{_libdir}/libsvrcore.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libsvrcore.la

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post -n %{libpackage} -p /sbin/ldconfig

%postun -n %{libpackage} -p /sbin/ldconfig

%files -n %{libpackage}
%defattr(-,root,root,-)
%{_libdir}/libsvrcore.so.*

%files devel
%defattr(-,root,root,-)
%doc LICENSE README NEWS
%{_libdir}/pkgconfig/svrcore.pc
%{_libdir}/libsvrcore.so
%{_includedir}/svrcore.h

%changelog
