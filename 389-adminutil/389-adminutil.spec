#
# spec file for package 389-adminutil
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


Summary:        Utility library for 389 administration
License:        LGPL-2.0
Group:          Development/Libraries/Other
Name:           389-adminutil
Version:        1.1.20
Release:        0
Url:            http://port389.org/wiki/AdminUtil

#DL-URL:        http://port389.org/sources/%%{name}-%%{version}.tar.bz2
Source:         %{name}-%{version}.tar.bz2
BuildRequires:  gcc-c++
BuildRequires:  icu
%if 0%{?suse_version} >= 1100
BuildRequires:  fdupes
%endif
BuildRequires:  libicu-devel
BuildRequires:  mozilla-nspr-devel
BuildRequires:  mozilla-nss-devel
BuildRequires:  openldap2-devel
BuildRequires:  svrcore-devel
#BuildRequires:  xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

Requires:       icu
Requires:       libadminutil0 = %{version}
Requires:       libadmsslutil0 = %{version}
Requires:       %{name}-lang = %{version}

%description
389-adminutil is a set libraries of functions used to administer
directory servers, usually in conjunction with the admin server.
389-adminutil is broken into two libraries - libadminutil contains
the basic functionality, and libadmsslutil contains SSL versions and
wrappers around the basic functions. The PSET functions allow
applications to store their preferences and configuration parameters
in LDAP, without having to know anything about LDAP. The
configuration is cached in a local file, allowing applications to
function even if the LDAP server is down. The other code is typically
used by CGI programs used for directory server management, containing
GET/POST processing code as well as resource handling (ICU ures API).


%package -n libadminutil0
Summary:        Utility libraries for the 389 Admin Server
Group:          System/Libraries

%description -n libadminutil0
389-adminutil is a set libraries of functions used to administer
directory servers, usually in conjunction with the admin server.
389-adminutil is broken into two libraries, and libadminutil contains
the basic functionality.


%package -n libadmsslutil0
Summary:        Utility libraries for the 389 Admin Server
Group:          System/Libraries

%description -n libadmsslutil0
389-adminutil is a set libraries of functions used to administer
directory servers, usually in conjunction with the admin server.
This library contains SSL wrappers around the functions in libadminutil.


%package devel
Summary:        Development and header files for 389-adminutil
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}
Requires:       libicu-devel
Requires:       mozilla-nspr-devel
Requires:       mozilla-nss-devel
Requires:       openldap2-devel
Requires:       pkgconfig
Requires:       svrcore-devel

%description devel
389-adminutil is a set libraries of functions used to administer
directory servers, usually in conjunction with the admin server.
389-adminutil is broken into two libraries - libadminutil contains
the basic functionality, and libadmsslutil contains SSL versions and
wrappers around the basic functions. The PSET functions allow
applications to store their preferences and configuration parameters
in LDAP, without having to know anything about LDAP. The
configuration is cached in a local file, allowing applications to
function even if the LDAP server is down. The other code is typically
used by CGI programs used for directory server management, containing
GET/POST processing code as well as resource handling (ICU ures API).


%package lang
Summary:        Languages for package %{name}
Group:          System/Localization
%if 0%{?sles_version} != 11
# SLE 11 uses RPM 4.4, noarch subpackges are not supported by RPM < 4.6
BuildArch:      noarch
%endif
Provides:       %{name}-lang-all = %{version}
Supplements:    packageand(bundle-lang-other:%{version})

%description lang
Provides translations to the package %{name}.


%prep
%setup -q

%build
%{configure} --disable-static --disable-tests --with-openldap
%{__make} %{?_smp_mflags}

%install
%{__make} install DESTDIR="%{buildroot}"
rm -f "%{buildroot}/%{_libdir}"/*.la

# fdupes
%if 0%{?suse_version} >= 1100
%fdupes %{buildroot}
%endif

%post   -n libadminutil0 -p /sbin/ldconfig
%postun -n libadminutil0 -p /sbin/ldconfig
%post   -n libadmsslutil0 -p /sbin/ldconfig
%postun -n libadmsslutil0 -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc LICENSE README NEWS

%files -n libadminutil0
%defattr(-,root,root)
%{_libdir}/libadminutil.so.0*

%files -n libadmsslutil0
%defattr(-,root,root)
%{_libdir}/libadmsslutil.so.0*

%files lang
%defattr(-,root,root)
%{_datadir}/%{name}

%files devel
%defattr(-,root,root)
%{_includedir}/libadminutil
%{_includedir}/libadmsslutil
%{_libdir}/libadminutil.so
%{_libdir}/libadmsslutil.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
