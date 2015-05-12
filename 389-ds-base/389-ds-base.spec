#
# spec file for package 389-ds-base
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


%if 0%{?sles_version} == 11
%global with_systemd 0
%else
%global with_systemd 1
%endif

Name:           389-ds-base
Summary:        389 Directory Server
Version:        1.2.11.30
Release:        0

Group:          Productivity/Networking/LDAP/Servers
License:        GPL-2.0
Url:            http://port389.org/
#DL-URL:        http://port389.org/wiki/Source
#Git-Clone:     git://git.fedorahosted.org/389/ds
Source:         http://port389.org/sources/%{name}-%{version}.tar.bz2
# Patch1: Make init scripts LSB conform
Patch1:         389-ds-base-1.2.11.15_dirsrv_init.patch
# Patch2: Fix Kolab bug 2229
Patch2:         fix-sasl-path.diff

BuildRequires:  bzip2
BuildRequires:  cyrus-sasl-devel >= 2.1.19
BuildRequires:  gcc-c++
BuildRequires:  krb5-devel
BuildRequires:  db-devel >= 4.5
# net-snmp-devel is needed to build the snmp ldap-agent
BuildRequires:  net-snmp-devel >= 5.1.2
BuildRequires:  openldap2-devel
# pam-devel is required the pam passthru auth plug-in
BuildRequires:  pam-devel
%if 0%{?sles_version}
BuildRequires:  libicu-devel >= 3.4
BuildRequires:  mozilla-nspr-devel >= 4.6.4
BuildRequires:  mozilla-nss-devel >= 3.11.4
BuildRequires:  pcre-devel
BuildRequires:  svrcore-devel >= 4.0.3
%else
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(libpcre)
BuildRequires:  pkgconfig(nspr)
BuildRequires:  pkgconfig(nss)
BuildRequires:  pkgconfig(svrcore)
BuildRequires:  pkgconfig(systemd)
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

Requires:       perl-Mozilla-LDAP

%if %{?with_systemd} == 0
# for the init script
Requires(post):   insserv
Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/chkconfig
Requires(preun):  /sbin/service
%else
# for systemd
%{?systemd_requires}
%endif
%if 0%{?suse_version}
Requires(post): fillup
%endif

Obsoletes:      389-ds < %{version}
Provides:       389-ds = %{version}

Recommends:     389-admin

%description
389 Directory Server is a full-featured LDAPv3 compliant server. In
addition to the standard LDAPv3 operations, it supports multi-master
replication, fully online configuration and administration, chaining,
virtual attributes, access control directives in the data, Virtual
List View, server-side sorting, SASL, TLS/SSL, and many other
features.


%package devel
Summary:        Development files for the 389 Directory Server
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}-%{release}

%description devel
389 Directory Server is a full-featured LDAPv3 compliant server. In
addition to the standard LDAPv3 operations, it supports multi-master
replication, fully online configuration and administration, chaining,
virtual attributes, access control directives in the data, Virtual
List View, server-side sorting, SASL, TLS/SSL, and many other
features.

This package contains the development files for 389-ds.


%prep
%setup -q
%patch1 -p 0

%build
# openldap has no pkgconfig file; because of that, 389-ds will prefer
# mozldap. Force use of openldap.
%{configure} --enable-autobind \
             --with-openldap \
%if %{?with_systemd} == 1
             --with-systemdsystemunitdir \
             --with-systemdsystemconfdir \
             --with-systemdgroupname=dirsrv.target \
%else
             --with-initddir=%{_initddir} \
%endif
           ..
%{__make} %{?_smp_mflags};

%install
%{__make} install DESTDIR=%{buildroot};
find %{buildroot}/%{_libdir} -type f -name "*.la" -delete;

%if %{?with_systemd} == 1
# systemd directory used for instances created with setup
%{__install} -d %{buildroot}%{_unitdir}/dirsrv.target.wants
%endif

%if 0%{?suse_version}
mkdir -p %{buildroot}/%{_localstatedir}/adm/fillup-templates;
for i in %{buildroot}/%{_sysconfdir}/sysconfig/*; do
  mv $i %{buildroot}/%{_localstatedir}/adm/fillup-templates/sysconfig.${i##*/};
done;
%endif

%if %{?with_systemd} == 1
%pre
%service_add_pre dirsrv@*.service dirsrv-snmp.service dirsrv.target
%endif

%post
/sbin/ldconfig
%if %{?with_systemd} == 1
%if 0%{?suse_version}
%fillup_only -n dirsrv
%fillup_only -n dirsrv.systemd
%endif
%service_add_post dirsrv@*.service dirsrv-snmp.service dirsrv.target
%else
%fillup_and_insserv dirsrv
%endif

%preun
%if %{?with_systemd} == 1
%service_del_preun dirsrv@*.service dirsrv-snmp.service dirsrv.target
%else
%stop_on_removal dirsrv
%endif

%postun
/sbin/ldconfig
%if %{?with_systemd} == 1
%service_del_postun dirsrv@*.service dirsrv-snmp.service dirsrv.target
%else
%restart_on_update dirsrv
%insserv_cleanup
%endif

%files
%defattr(-,root,root)
%config %{_sysconfdir}/dirsrv
%{_bindir}/*
%dir %{_libdir}/dirsrv
%{_libdir}/dirsrv/*.so.*
%dir %{_libdir}/dirsrv/perl
%{_libdir}/dirsrv/perl/*.pm
%dir %{_libdir}/dirsrv/plugins
%{_libdir}/dirsrv/plugins/*.so
%{_sbindir}/*
%{_datadir}/dirsrv
%{_mandir}/man?/*
%if 0%{?suse_version}
%{_localstatedir}/adm/fillup-templates/sysconfig.*
%else
%{_sysconfdir}/sysconfig/*
%endif
%if %{?with_systemd} == 1
%{_unitdir}/dirsrv*
%else
%{_initddir}/*
%endif

%files devel
%defattr(-,root,root)
%{_includedir}/dirsrv
%{_libdir}/dirsrv/*.so
%{_libdir}/pkgconfig/dirsrv.pc

%changelog
