# Exclude i686 bit arches
ExcludeArch: i686

%define nspr_name       nspr
%define nspr_version    4.6
%define nss_name        nss
%define nss_version     3.11
%define svrcore_name    svrcore
%define svrcore_version 4.0.3

%define major           6
%define minor           0
%define submin          7
%define libsuffix       %{major}0

Summary:          Mozilla LDAP C SDK
Name:             mozldap
Version:          %{major}.%{minor}.%{submin}
Release:          27.13%{?dist}.kolab_wf
License:          MPLv1.1 or GPLv2+ or LGPLv2+
URL:              http://www.mozilla.org/directory/csdk.html
Requires:         %{nspr_name} >= %{nspr_version}
Requires:         %{nss_name} >= %{nss_version}
Requires:         %{svrcore_name} >= %{svrcore_version}
BuildRequires:    %{nspr_name}-devel >= %{nspr_version}
BuildRequires:    %{nss_name}-devel >= %{nss_version}
BuildRequires:    %{svrcore_name}-devel >= %{svrcore_version}
BuildRequires:    gcc-c++
BuildRequires:    cyrus-sasl-devel
BuildRequires:    perl

Source0:          ftp://ftp.mozilla.org/pub/mozilla.org/directory/c-sdk/releases/v%{version}/src/%{name}-%{version}.tar.gz
Patch0:           support-tls1.1-and-later.patch 

%description
The Mozilla LDAP C SDK is a set of libraries that
allow applications to communicate with LDAP directory
servers.  These libraries are derived from the University
of Michigan and Netscape LDAP libraries.  They use Mozilla
NSPR and NSS for crypto.


%package tools
Summary:          Tools for the Mozilla LDAP C SDK
Requires:         %{name} = %{version}-%{release}
BuildRequires:    %{nspr_name}-devel >= %{nspr_version}
BuildRequires:    %{nss_name}-devel >= %{nss_version}
BuildRequires:    %{svrcore_name}-devel >= %{svrcore_version}

%description tools
The mozldap-tools package provides the ldapsearch,
ldapmodify, and ldapdelete tools that use the
Mozilla LDAP C SDK libraries.


%package devel
Summary:          Development libraries and examples for Mozilla LDAP C SDK
Requires:         %{name} = %{version}-%{release}
Requires:         %{nspr_name}-devel >= %{nspr_version}
Requires:         %{nss_name}-devel >= %{nss_version}
Requires:         %{svrcore_name}-devel >= %{svrcore_version}
Requires:         pkgconfig

%description devel
Header and Library files for doing development with the Mozilla LDAP C SDK

%prep
%setup -q
%patch0 -p1

%build
cd c-sdk

%configure \
%ifarch x86_64 ppc64 ia64 s390x sparc64
    --enable-64bit \
%endif
    --with-sasl \
    --enable-clu \
    --with-system-svrcore \
    --enable-optimize \
    --disable-debug

# Enable compiler optimizations and disable debugging code
BUILD_OPT=1
export BUILD_OPT

# Generate symbolic info for debuggers
XCFLAGS="$RPM_OPT_FLAGS"
export XCFLAGS

PKG_CONFIG_ALLOW_SYSTEM_LIBS=1
PKG_CONFIG_ALLOW_SYSTEM_CFLAGS=1

export PKG_CONFIG_ALLOW_SYSTEM_LIBS
export PKG_CONFIG_ALLOW_SYSTEM_CFLAGS

make \
%ifarch x86_64 ppc64 ia64 s390x sparc64
    USE_64=1
%endif

%install
%{__rm} -rf $RPM_BUILD_ROOT

# Set up our package file
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/pkgconfig
%{__cat} c-sdk/mozldap.pc.in \
    | sed -e "s,%%libdir%%,%{_libdir},g" \
          -e "s,%%prefix%%,%{_prefix},g" \
          -e "s,%%major%%,%{major},g" \
          -e "s,%%minor%%,%{minor},g" \
          -e "s,%%submin%%,%{submin},g" \
          -e "s,%%libsuffix%%,%{libsuffix},g" \
          -e "s,%%bindir%%,%{_libdir}/%{name},g" \
          -e "s,%%exec_prefix%%,%{_prefix},g" \
          -e "s,%%includedir%%,%{_includedir}/%{name},g" \
          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
          -e "s,%%NSS_VERSION%%,%{nss_version},g" \
          -e "s,%%SVRCORE_VERSION%%,%{svrcore_version},g" \
          -e "s,%%MOZLDAP_VERSION%%,%{version},g" \
    > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/%{name}.pc

# There is no make install target so we'll do it ourselves.

%{__mkdir_p} $RPM_BUILD_ROOT%{_includedir}/%{name}
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/%{name}

# Copy the binary libraries we want
for file in libssldap%{libsuffix}.so libprldap%{libsuffix}.so libldap%{libsuffix}.so libldif%{libsuffix}.so
do
  %{__install} -m 755 $(find c-sdk/ -type f -name "$file") $RPM_BUILD_ROOT%{_libdir}
done

# Copy the binaries we want
for file in ldapsearch ldapmodify ldapdelete ldapcmp ldapcompare ldappasswd
do
  %{__install} -m 755 $(find c-sdk/ -type f -name "$file") $RPM_BUILD_ROOT%{_libdir}/%{name}
done

# Copy the include files
for file in c-sdk/ldap/include/*.h
do
  %{__install} -p -m 644 $file $RPM_BUILD_ROOT%{_includedir}/%{name}
done

# Copy the developer files
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -r c-sdk/ldap/examples $RPM_BUILD_ROOT%{_datadir}/%{name}
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/%{name}/etc
%{__install} -m 644 c-sdk/ldap/examples/xmplflt.conf $RPM_BUILD_ROOT%{_datadir}/%{name}/etc
%{__install} -m 644 c-sdk/ldap/libraries/libldap/ldaptemplates.conf $RPM_BUILD_ROOT%{_datadir}/%{name}/etc
%{__install} -m 644 c-sdk/ldap/libraries/libldap/ldapfilter.conf $RPM_BUILD_ROOT%{_datadir}/%{name}/etc
%{__install} -m 644 c-sdk/ldap/libraries/libldap/ldapsearchprefs.conf $RPM_BUILD_ROOT%{_datadir}/%{name}/etc


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc c-sdk/README.rpm
%{_libdir}/libssldap*.so
%{_libdir}/libprldap*.so
%{_libdir}/libldap*.so
%{_libdir}/libldif*.so

%files tools
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/ldapsearch
%{_libdir}/%{name}/ldapmodify
%{_libdir}/%{name}/ldapdelete
%{_libdir}/%{name}/ldapcmp
%{_libdir}/%{name}/ldapcompare
%{_libdir}/%{name}/ldappasswd

%files devel
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}
%{_datadir}/%{name}

%changelog
* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.5-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 4 2019 Mark Reynolds <mreynolds@redhat.com> - 6.0.5-24
- Bump version to 6.0.5-24
- Add perl build requirement and stop building i686 because of no srvcore

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.5-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.5-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.5-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.5-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.5-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.5-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.5-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 6.0.5-15
- Rebuilt for GCC 5 C++11 ABI change

* Mon Nov  3 2014 Noriko Hosoi <nhosoi@redhat.com> - 6.0.5-14
- Disable SSL3
- Support TLS 1.1 and newer using the NSS Version Range APIs.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Aug 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 6.0.5-4
- actually fix license tag (whoops)

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 6.0.5-3
- fix license tag
- enable sparc64

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 6.0.5-2
- Autorebuild for GCC 4.3

* Wed Sep 26 2007 Rich Megginson <rmeggins@redhat.com> - 6.0.5-1
- bump to version 6.0.5 - this version allows the use of SASL
- with IPv6 numeric addresses, as well as some memory leak fixes

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 6.0.4-2
- Rebuild for selinux ppc32 issue.

* Wed Jun 20 2007 Rich Megginson <rmeggins@redhat.com> - 6.0.4-1
- bump version to 6.0.4 - this version has some memory leak
- fixes for SASL related code, fixes for control handling with
- referral chasing, and packaging improvements
- use -p when installing include files to preserve timestamps

* Thu May 24 2007 Rich Megginson <rmeggins@redhat.com> - 6.0.3-3
- We only need cyrus-sasl-devel as a BuildRequires in the main package

* Mon May 21 2007 Rich Megginson <rmeggins@redhat.com> - 6.0.3-2
- added cyrus-sasl-devel and pkgconfig to devel package Requires

* Tue Mar 13 2007 Rich Megginson <richm@stanfordalumni.org> - 6.0.3-1
- bumped version to 6.0.3
- minor build fixes for some platforms

* Mon Jan 15 2007 Rich Megginson <richm@stanfordalumni.org> - 6.0.2-1
- Fixed exports file generation for Solaris and Windows - no effect on linux
- bumped version to 6.0.2

* Tue Jan  9 2007 Rich Megginson <richm@stanfordalumni.org> - 6.0.1-2
- Remove buildroot = "/" checking
- Remove buildroot removal from %%build section

* Mon Jan  8 2007 Rich Megginson <richm@stanfordalumni.org> - 6.0.1-1
- bump version to 6.0.1
- added libldif and ldif.h

* Fri Dec  8 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 6.0.0-2
- Rename to mozldap.
- move configure step to %%build section.
- clean up excessive use of %%defines, make more Fedora like.
- fix mismatching soname issue.
- generic specfile cosmetics.

* Thu Oct  5 2006 Rich Megginson <richm@stanforalumni.org> - 6.0.0-1
- Bump version to 6.0.0 - add support for submit/patch level (3rd level) in version numbering

* Tue Apr 18 2006 Richard Megginson <richm@stanforalumni.org> - 5.17-3
- make more Fedora Core friendly - move each requires and buildrequires to a separate line
- remove --with-nss since svrcore implies it; fix some macro errors; macro-ize nspr and nss names
- fix directory attrs in devel package

* Tue Jan 31 2006 Rich Megginson <rmeggins@redhat.com> - 5.17-2
- use --with-system-svrcore to configure

* Mon Dec 19 2005 Rich Megginson <rmeggins@redhat.com> - 5.17-1
- Initial revision

