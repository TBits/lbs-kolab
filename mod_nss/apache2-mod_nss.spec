#
# spec file for package apache2-mod_nss
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


Name:           apache2-mod_nss
Summary:        SSL/TLS module for the Apache HTTP server
License:        Apache-2.0
Group:          Productivity/Networking/Web/Servers
Version:        1.0.8
Release:        0
Url:            http://directory.fedoraproject.org/wiki/Mod_nss
Source:         http://directory.fedoraproject.org/sources/mod_nss-%{version}.tar.gz
Provides:       mod_nss
Requires:       apache2 >= 2.0.52
Requires:       findutils
Requires(post): mozilla-nss-tools
BuildRequires:  apache2-devel >= 2.0.52
BuildRequires:  bison
BuildRequires:  findutils
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  libapr-util1-devel
BuildRequires:  libapr1-devel
BuildRequires:  mozilla-nspr-devel >= 4.6.3
BuildRequires:  mozilla-nss-devel >= 3.12.6
BuildRequires:  pkgconfig
# [bnc#799483] Patch to adjust mod_nss.conf to match SUSE dir layout
Patch1:         mod_nss-conf.patch
Patch2:         mod_nss-gencert.patch
Patch3:         mod_nss-wouldblock.patch
Patch4:         mod_nss-negotiate.patch
Patch5:         mod_nss-reverseproxy.patch
Patch6:         mod_nss-pcachesignal.h
Patch7:         mod_nss-reseterror.patch
Patch8:         mod_nss-lockpcache.patch
# Fix build with apache 2.4
Patch9:         mod_nss-httpd24.patch

Patch10:        mod_nss-proxyvariables.patch
Patch11:        mod_nss-tlsv1_1.patch
Patch12:        mod_nss-array_overrun.patch
Patch13:        mod_nss-clientauth.patch
Patch14:        mod_nss-no_shutdown_if_not_init_2.patch
Patch15:        mod_nss-PK11_ListCerts_2.patch
Patch16:        mod_nss-sslmultiproxy.patch
Patch17:        mod_nss-overlapping_memcpy.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%define    apxs /usr/sbin/apxs2
%define    apache apache2
%define    apache_libexecdir %(%{apxs} -q LIBEXECDIR)
%define    apache_sysconfdir %(%{apxs} -q SYSCONFDIR)
%define    apache_includedir %(%{apxs} -q INCLUDEDIR)
%define    apache_serverroot %(%{apxs} -q PREFIX)
%define    apache_mmn        %(MMN=$(%{apxs} -q LIBEXECDIR)_MMN; test -x $MMN && $MMN)

%description
The mod_nss module provides strong cryptography for the Apache Web
server via the Secure Sockets Layer (SSL) and Transport Layer
Security (TLS) protocols using the Network Security Services (NSS)
security library.

%prep
%setup -q -n mod_nss-%{version}
%patch1 -p1 -b .conf
%patch2 -p1 -b .gencert
%patch3 -p1 -b .wouldblock
%patch4 -p1 -b .negotiate
%patch5 -p1 -b .reverseproxy
%patch6 -p1 -b .pcachesignal.h
%patch7 -p1 -b .reseterror
%patch8 -p1 -b .lockpcache
%patch10 -p1 -b .proxyvariables
%patch11 -p1 -b .tlsv1_1
%patch12 -p1 -b .array_overrun
%patch13 -p1 -b .clientauth.patch
%patch14 -p1 -b .no_shutdown_if_not_init_2
%patch15 -p1 -b .PK11_ListCerts_2
%patch16 -p1 -b .sslmultiproxy
%patch17 -p1 -b .overlapping_memcpy

# keep this last, otherwise we get fuzzyness from above
%if 0%{?suse_version} >= 1300
%patch9 -p1 -b .http24
%endif

# Touch expression parser sources to prevent regenerating it
touch nss_expr_*.[chyl]

%build
CFLAGS="$RPM_OPT_FLAGS"
export CFLAGS
NSPR_INCLUDE_DIR=`/usr/bin/pkg-config --variable=includedir nspr`
NSPR_LIB_DIR=`/usr/bin/pkg-config --variable=libdir nspr`
NSS_INCLUDE_DIR=`/usr/bin/pkg-config --variable=includedir nss`
NSS_LIB_DIR=`/usr/bin/pkg-config --variable=libdir nss`
NSS_BIN=`/usr/bin/pkg-config --variable=exec_prefix nss`
# For some reason mod_nss can't find nss on SUSE unless we do the following
C_INCLUDE_PATH="/usr/include/nss3:/usr/include/nspr4:/usr/include/apache2-prefork/"
export C_INCLUDE_PATH
#autoreconf -fvi
%configure \
    --with-nss-lib=$NSS_LIB_DIR \
    --with-nss-inc=$NSS_INCLUDE_DIR \
    --with-nspr-lib=$NSPR_LIB_DIR \
    --with-nspr-inc=$NSPR_INCLUDE_DIR \
    --with-apxs=%{apxs} \
    --with-apr-config
make %{?_smp_mflags} all

%install
# The install target of the Makefile isn't used because that uses apxs
# which tries to enable the module in the build host httpd instead of in
# the build root.
mkdir -p $RPM_BUILD_ROOT/%{apache_libexecdir}
mkdir -p $RPM_BUILD_ROOT%{apache_sysconfdir}/conf.d
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{apache_sysconfdir}/alias

%if 0%{?suse_version}
perl -pi -e "s|\@apache_lib\@|%{_libdir}\/apache2|g" nss.conf
%endif

install -m 644 nss.conf $RPM_BUILD_ROOT%{apache_sysconfdir}/conf.d/
install -m 755 .libs/libmodnss.so $RPM_BUILD_ROOT%{apache_libexecdir}
install -m 755 nss_pcache $RPM_BUILD_ROOT%{_sbindir}/
install -m 755 gencert $RPM_BUILD_ROOT%{_sbindir}/

#ln -s $RPM_BUILD_ROOT/%%{apache_libexecdir}/libnssckbi.so $RPM_BUILD_ROOT%%{apache_sysconfdir}/alias/
touch $RPM_BUILD_ROOT%{apache_sysconfdir}/alias/secmod.db
touch $RPM_BUILD_ROOT%{apache_sysconfdir}/alias/cert8.db
touch $RPM_BUILD_ROOT%{apache_sysconfdir}/alias/key3.db
touch $RPM_BUILD_ROOT%{apache_sysconfdir}/alias/install.log
perl -pi -e "s:$NSS_LIB_DIR:$NSS_BIN:" $RPM_BUILD_ROOT%{_sbindir}/gencert

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 077
if [ "$1" -eq 1 ] ; then
    if [ ! -e %{apache_sysconfdir}/alias/key3.db ]; then
        %{_sbindir}/gencert %{apache_sysconfdir}/alias > %{apache_sysconfdir}/alias/install.log 2>&1
        echo ""
        echo "%{name} certificate database generated."
        echo ""
    fi
    # Make sure that the database ownership is setup properly.
    find %{apache_sysconfdir}/alias -user root -name "*.db" -exec /bin/chgrp www {} \;
    find %{apache_sysconfdir}/alias -user root -name "*.db" -exec /bin/chmod g+r {} \;
fi

%files
%defattr(-,root,root,-)
%doc README LICENSE docs/mod_nss.html
%config(noreplace) %{apache_sysconfdir}/conf.d/nss.conf
%dir %{apache_libexecdir}
%{apache_libexecdir}/libmodnss.so
%dir %{apache_sysconfdir}/alias/
%ghost %attr(0640,root,www) %config(noreplace) %{apache_sysconfdir}/alias/secmod.db
%ghost %attr(0640,root,www) %config(noreplace) %{apache_sysconfdir}/alias/cert8.db
%ghost %attr(0640,root,www) %config(noreplace) %{apache_sysconfdir}/alias/key3.db
%ghost %config(noreplace) %{apache_sysconfdir}/alias/install.log
#%%{apache_sysconfdir}/alias/libnssckbi.so
%{_sbindir}/nss_pcache
%{_sbindir}/gencert

%changelog
