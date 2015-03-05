#
# spec file for package mozilla-jss
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


Name:           mozilla-jss
Version:        4.3.2
Release:        2%{?dist}
Summary:        Java Security Services (JSS)
Group:          Development/Libraries/Java
License:        MPL-1.1 or GPL-2.0+ or LGPL-2.0+
URL:            http://www.mozilla.org/projects/security/pki/jss/
# The source for this package was pulled from upstream's cvs. Use the
# following commands to generate the tarball:
# cvs -d :pserver:anonymous@cvs-mirror.mozilla.org:/cvsroot export -r JSS_4_3_2_RTM -d jss-4.3.2 -N mozilla/security/coreconf mozilla/security/jss
# tar cjvf jss-4.3.2.tar.gz jss-4.3.2
Source0:        jss-%{version}.tar.bz2
Source1:        MPL-1.1.txt
Source2:        gpl.txt
Source3:        lgpl.txt
BuildRequires:  pkg-config
BuildRequires:  mozilla-nss-devel >= 3.12.3.99
BuildRequires:  mozilla-nspr-devel >= 4.6.99
BuildRequires:  java-devel
Requires:       java
Requires:       mozilla-nss >= 3.12.3.99
Patch1:         jss-ipv6.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Java Security Services (JSS) is a java native interface which provides a bridge
for java-based applications to use native Network Security Services (NSS).
This only works with gcj. Other JREs require that JCE providers be signed.

%package javadoc
Summary:        Java Security Services (JSS) Javadocs
Group:          Development/Libraries/Java
Requires:       mozilla-jss = %{version}-%{release}

%description javadoc
This package contains the API documentation for JSS.

%prep
%setup -q -n jss-%{version}
%patch1

%build
[ -z "$JAVA_HOME" ] && export JAVA_HOME=%{_jvmdir}/java
# Enable compiler optimizations and disable debugging code
BUILD_OPT=1
export BUILD_OPT
# Generate symbolic info for debuggers
XCFLAGS="-g $RPM_OPT_FLAGS"
export XCFLAGS
PKG_CONFIG_ALLOW_SYSTEM_LIBS=1
PKG_CONFIG_ALLOW_SYSTEM_CFLAGS=1
export PKG_CONFIG_ALLOW_SYSTEM_LIBS
export PKG_CONFIG_ALLOW_SYSTEM_CFLAGS
NSPR_INCLUDE_DIR=`/usr/bin/pkg-config --cflags-only-I nspr | sed 's/-I//'`
NSPR_LIB_DIR=`/usr/bin/pkg-config --libs-only-L nspr | sed 's/-L//'`
NSS_INCLUDE_DIR=`/usr/bin/pkg-config --cflags-only-I nss | sed 's/-I//'`
NSS_LIB_DIR=`/usr/bin/pkg-config --libs-only-L nss | sed 's/-L//'`
export NSPR_INCLUDE_DIR
export NSPR_LIB_DIR
export NSS_INCLUDE_DIR
export NSS_LIB_DIR
%ifarch x86_64 ppc64 ia64 s390x sparc64
USE_64=1
export USE_64
%endif
# Fix for Kernel >= 3 (autoget kernel version
%if 0%{?suse_version} >= 1210
%global majorrel `uname -r | cut -f1 -d.`
%global minorrel `uname -r | cut -f2 -d.`
cp -p mozilla/security/coreconf/Linux2.6.mk mozilla/security/coreconf/Linux%{majorrel}.%{minorrel}.mk || :
sed -i -e 's;LINUX2_1;LINUX{%minorrel}_%{minorrel};' mozilla/security/coreconf/Linux%{majorrel}.%{minorrel}.mk
%endif
# For some reason jss can't find nss on SUSE unless we do the following
C_INCLUDE_PATH="/usr/include/nss3:/usr/include/nspr4"
export C_INCLUDE_PATH
# The Makefile is not thread-safe
make -C mozilla/security/coreconf
make -C mozilla/security/jss
make -C mozilla/security/jss javadoc

%install
# Supress SUSE bytecode version error check
export NO_BRP_CHECK_BYTECODE_VERSION=true
# Copy the license files here so we can include them in %doc
cp -p %{SOURCE1} .
cp -p %{SOURCE2} .
cp -p %{SOURCE3} .

# There is no install target so we'll do it by hand
# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_jnidir}
install -m 644 mozilla/dist/xpclass.jar ${RPM_BUILD_ROOT}%{_jnidir}/jss4-%{version}.jar
pushd  $RPM_BUILD_ROOT%{_jnidir}
    ln -fs jss4-%{version}.jar jss4.jar
popd

# We have to use the name libjss4.so because this is dynamically
# loaded by the jar file.
install -d -m 0755 $RPM_BUILD_ROOT%{_libdir}
install -m 0755 mozilla/dist/Linux*.OBJ/lib/libjss4.so ${RPM_BUILD_ROOT}%{_libdir}/

# FIXME - sign jss4.jar. In order to use JSS as a JCE provider it needs to be
# signed with a Sun-issued certificate. Since we would need to make this
# certificate and private key public to provide reproducability in the rpm
# building we have to ship an unsigned jar.
#
# Instructions for getting a signing cert can be found here:
# http://java.sun.com/javase/6/docs/technotes/guides/security/crypto/HowToImplAProvider.html#Step61
#
# This signing is not required by every JVM. gcj ignores the signature and does
# not require one. The Sun and IBM JVMs both check and enforce the signature.
# Behavior of other JVMs is not known but they probably enforce the signature
# as well.

# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -rp mozilla/dist/jssdoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
rm $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/index.html.bak

%clean
rm -rf $RPM_BUILD_ROOT

# No ldconfig is required since this library is loaded by Java itself.
%files
%defattr(-,root,root,-)
%doc mozilla/security/jss/jss.html MPL-1.1.txt gpl.txt lgpl.txt
%if 0%{?suse_version}
%dir %{_jnidir}
%endif
%{_jnidir}/*
%{_libdir}/lib*.so

%files javadoc
%defattr(-,root,root,-)
%if 0%{?suse_version}
%dir %{_javadocdir}
%endif
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*

%changelog

