#
# spec file for package 389-admin
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


%define pkgname   dirsrv
%define apxs /usr/sbin/apxs2
# systemd support
%global groupname %{pkgname}.target

%if 0%{?sles_version} == 11
%global with_systemd 0
%else
%global with_systemd 1
%endif

Summary:          389 Administration Server (admin)
Name:             389-admin
Version:          1.1.31
Release:          0
License:          GPL-2.0 and Apache-2.0
Url:              http://port389.org/
Group:            Productivity/Networking/LDAP/Utilities

Source0:          http://port389.org/wiki/Source/%{name}-%{version}.tar.bz2
# 389-admin_initscript_lsb.diff: Add LSB headers to dirsrv-admin init script
Patch1:           389-admin_initscript_lsb.diff
Patch2:           389-admin_restartsrv.diff
# 389-admin_httpd_conf.diff: listen on port 8080 to prevent collision
Patch3:           389-admin_httpd_conf.diff
BuildRequires:    389-adminutil-devel
BuildRequires:    apache2
BuildRequires:    apache2-devel
BuildRequires:    apache2-mod_nss
BuildRequires:    cyrus-sasl-devel
%if 0%{?suse_version} >= 1100
BuildRequires:    fdupes
%endif
BuildRequires:    gcc-c++
BuildRequires:    icu
BuildRequires:    libapr1-devel
BuildRequires:    libicu-devel
BuildRequires:    libapr1-devel
BuildRequires:    mozilla-nspr-devel
BuildRequires:    mozilla-nss-devel
BuildRequires:    openldap2-devel
BuildRequires:    svrcore-devel
%if %{?with_systemd} == 1
BuildRequires:    systemd
%endif
BuildRoot:        %{_tmppath}/%{name}-%{version}-build

Requires:         389-ds-base
Requires:         apache2-mod_nss
# the following are needed for some of our scripts
Requires:         mozilla-nss-tools
Requires:         perl-Mozilla-LDAP
# this is needed for using semanage from our setup scripts
Requires:         policycoreutils-python

%if %{?with_systemd} == 0
# for the init script
Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/chkconfig
Requires(preun):  /sbin/service
%else
# for systemd
%{?systemd_requires}
%endif

%description
389 Administration Server is an HTTP agent that provides management features
for 389 Directory Server.  It provides some management web apps that can
be used through a web browser.  It provides the authentication, access control,
and CGI utilities used by the console.


%package -n libds-admin-serv0
Summary:          Libraries for the 389 Admin Server
Group:            System/Libraries

%description -n libds-admin-serv0
389 Administration Server is an HTTP agent that provides management features
for 389 Directory Server.  It provides some management web apps that can
be used through a web browser.  It provides the authentication, access control,
and CGI utilities used by the console.

389-adminutil is broken into two libraries, and libadminutil contains
the basic functionality.


%prep
%setup -q
%if %{?with_systemd} == 0
%patch1 -p0
%endif
%patch2 -p0
%patch3 -p0

%build
%configure \
    --with-adminutil=/usr/ \
    --with-apr-config \
    --with-apxs=%{apxs} \
    --with-httpd=/usr/sbin/httpd2 \
    --with-openldap \
    --with-selinux \
%if %{?with_systemd} == 0
    --with-initddir=/etc/init.d/ \
    --enable-service \
%else
    --with-systemddirsrvgroupname=%{groupname} \
    --with-systemdsystemunitdir=%{_unitdir} \
%endif
    --disable-rpath \
    --disable-threading \
    .

# Generate symbolic info for debuggers
export XCFLAGS=$RPM_OPT_FLAGS

%ifarch x86_64 ppc64 ia64 s390x sparc64
export USE_64=1
%endif

%{__make} %{?_smp_mflags}

%install
%{__make} DESTDIR="%{buildroot}" install

# make console jars directory
mkdir -p %{buildroot}%{_datadir}/%{pkgname}/html/java

mkdir -p %{buildroot}/var/adm/fillup-templates
mv %{buildroot}%{_sysconfdir}/sysconfig/dirsrv-admin %{buildroot}/var/adm/fillup-templates/sysconfig.dirsrv-admin

%if %{?with_systemd} == 0
ln -s %{_sysconfdir}/init.d/%{pkgname}-admin %{buildroot}%{_sbindir}/rc%{pkgname}-admin
%endif

#remove libtool and static libs
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.so
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/%{pkgname}/modules/*.a
rm -f %{buildroot}%{_libdir}/%{pkgname}/modules/*.la

# fdupes
%if 0%{?suse_version} >= 1100
%fdupes %{buildroot}%{_datadir}/%{pkgname}
%endif

%pre -p <lua>
-- save ownership/permissions on the dirs/files that rpm changes
-- if these don't exist, the vars will be nil
%{pkgname}admin_adminserv = posix.stat('%{_sysconfdir}/%{pkgname}/admin-serv')
%{pkgname}admin_consoleconf = posix.stat('%{_sysconfdir}/%{pkgname}/admin-serv/console.conf')

%post -p <lua>
-- do the usual daemon post setup stuff
if not posix.stat('%{_libdir}/apache2/mod_cgi.so') then
    if posix.stat('%{_libdir}/apache2-prefork/mod_cgi.so') then
        os.execute('ln -s %{_libdir}/apache2-prefork/mod_cgi.so %{_libdir}/apache2/mod_cgi.so')
    elseif posix.stat('%{_libdir}/apache2-worker/mod_cgi.so') then
        os.execute('ln -s %{_libdir}/apache2-worker/mod_cgi.so %{_libdir}/apache2/mod_cgi.so')
    elseif posix.stat('%{_libdir}/apache2-itk/mod_cgi.so') then
        os.execute('ln -s %{_libdir}/apache2-itk/mod_cgi.so %{_libdir}/apache2/mod_cgi.so')
    elseif posix.stat('%{_libdir}/apache2-event/mod_cgi.so') then
        os.execute('ln -s %{_libdir}/apache2-event/mod_cgi.so %{_libdir}/apache2/mod_cgi.so')
    end
end
%if %{?with_systemd} == 1
if not posix.stat('%{_sysconfdir}/sysconfig/%{pkgname}-admin') then
    os.execute('/bin/touch %{_sysconfdir}/sysconfig/%{pkgname}-admin')
    os.execute('/bin/fillup -q %{_sysconfdir}/sysconfig/%{pkgname}-admin %{_localstatedir}/adm/fillup-templates/sysconfig.%{pkgname}-admin')
end
os.execute('/bin/systemctl daemon-reload >/dev/null 2>&1 || :')
os.execute('/bin/systemctl preset %{pkgname}-admin.service >/dev/null 2>&1 || :')
%endif
os.execute('/sbin/ldconfig')
-- restore permissions if upgrading
if %{pkgname}admin_adminserv then
    posix.chmod('%{_sysconfdir}/%{pkgname}/admin-serv', %{pkgname}admin_adminserv.mode)
    posix.chown('%{_sysconfdir}/%{pkgname}/admin-serv', %{pkgname}admin_adminserv.uid, %{pkgname}admin_adminserv.gid)
end
if %{pkgname}admin_consoleconf then
    posix.chmod('%{_sysconfdir}/%{pkgname}/admin-serv/console.conf', %{pkgname}admin_consoleconf.mode)
    posix.chown('%{_sysconfdir}/%{pkgname}/admin-serv/console.conf', %{pkgname}admin_consoleconf.uid, %{pkgname}admin_consoleconf.gid)
end

%preun
%if %{?with_systemd} == 1
%service_del_preun %{pkgname}-admin.service
%else
%stop_on_removal %{pkgname}-admin
%endif

%postun
/sbin/ldconfig
%if %{?with_systemd} == 1
%service_del_postun %{pkgname}-admin.service
%else
%restart_on_update %{pkgname}-admin
%insserv_cleanup
%endif

%post   -n libds-admin-serv0 -p /sbin/ldconfig

%postun -n libds-admin-serv0 -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc LICENSE
%dir %{_sysconfdir}/%{pkgname}
%dir %{_sysconfdir}/%{pkgname}/admin-serv
%config(noreplace)%{_sysconfdir}/%{pkgname}/admin-serv/*.conf
%config(noreplace)%{_localstatedir}/adm/fillup-templates/sysconfig.%{pkgname}-admin
%{_datadir}/%{pkgname}
%if %{?with_systemd} == 0
%{_sysconfdir}/init.d/%{pkgname}-admin
%else
%{_unitdir}/%{pkgname}-admin.service
%endif
%{_sbindir}/*
%{_libdir}/%{pkgname}
%{_mandir}/man8/*
%{_libdir}/libds-admin-serv.so.*

%changelog
