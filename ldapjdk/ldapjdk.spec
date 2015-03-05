#
# spec file for package ldapjdk
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


Name:           ldapjdk
%define spname  ldapsp
Version:        4.18
Release:        0
Summary:        The Mozilla LDAP Java SDK
License:        MPL-1.1 and GPL-2.0 and LGPL-2.1
Group:          Development/Libraries/Java
Url:            http://www.mozilla.org/directory/javasdk.html
Source0:        http://pki.fedoraproject.org/pki/sources/ldapjdk/%{name}-%{version}.tar.gz
# mozilla-jss not available on openSUSE < 13.1, so we still require jss*.jar for build
# Mozilla Network Security Services for Java (JSS)
Source1:        jss4.jar
Patch1:         ldap-javasource14.patch
Patch2:         ldapjdk-jarnamefix.patch
Patch3:         matching-rule-parsing-640750.patch
BuildArch:      noarch
%if 0%{?suse_version} >= 1100
BuildRequires:  fdupes
%endif
BuildRequires:  java2-devel-packages
%if 0%{?suse_version} >= 1310
BuildRequires:  mozilla-jss
%endif
BuildRequires:  oro
BuildRequires:  xerces-j2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

Requires:       jaas
Requires:       jndi
Requires:       jpackage-utils >= 1.5
Requires:       jsse
Requires:       oro
# Provides:	jndi-ldap = 1.3.0

%description
The Mozilla LDAP SDKs enable you to write applications that access,
manage, and update the information stored in an LDAP directory.


%package javadoc
PreReq:         coreutils
Summary:        Javadoc for ldapjdk
Group:          Development/Libraries/Java
Obsoletes:      openjmx-javadoc

%description javadoc
The Mozilla LDAP SDKs enable you to write applications which access,
manage, and update the information stored in an LDAP directory.

This package contains the javadoc documentation for the Mozilla LDAP
SDKs.


%prep
%setup -q
%patch1
%patch2
%patch3

%build
# cleanup jars
rm -fr $(find . -name "*.jar"  -type f)
mv mozilla/directory/* .
rm -fr mozilla
cd java-sdk
if [ ! -e "$JAVA_HOME" ] ; then export JAVA_HOME="%{_jvmdir}/java" ; fi
%if %{?suse_version} >= 1310
export CLASSPATH=%{_jnidir}/jss4.jar:%(build-classpath oro)
%else
# mozilla-jss not available on openSUSE < 13.1, so we still require the .jar for build
cp %{SOURCE1} .
export CLASSPATH=`pwd`/jss4.jar:%(build-classpath oro)
%endif
export MOZ_SRC=`pwd`
export JAVA_VERSION=1.4
# Main jar
%__make -f ldap.mk clean
%__make -f ldap.mk
%__make -f ldap.mk basepackage
%__make -f ldap.mk doc
# ldap jdndi service provides
%__make -f ldapsp.mk clean
%__make -f ldapsp.mk
%__make -f ldapsp.mk basepackage
%__make -f ldapsp.mk doc

%install
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 java-sdk/dist/packages/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
install -m 644 java-sdk/dist/packages/%{spname}.jar %{buildroot}%{_javadir}/%{spname}-%{version}.jar
pushd %{buildroot}%{_javadir}
    for jar in *-%{version}.jar ; do
        ln -fs ${jar} $(echo $jar | sed "s|-%{version}.jar|.jar|g")
    done
popd
# install -d -m 755 %%{buildroot}%%{_javadir}-1.3.0
# 
# pushd %%{buildroot}%%{_javadir}-1.3.0
# 	ln -fs ../java/*%%name}.jar jndi-ldap.jar
# popd
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -r java-sdk/dist/doc/* %{buildroot}%{_javadocdir}/%{name}-%{version}

%if 0%{?suse_version} >= 1100
%fdupes %{buildroot}/%{_javadocdir}/%{name}-%{version}
%endif

%files
%defattr(0644,root,root,0755)
%doc buildjsdk.txt java-sdk/*.htm
%{_javadir}/%{name}*.jar
%{_javadir}/%{spname}*.jar
# %%{_javadir}-1.3.0/*.jar

%files javadoc
%defattr(0644,root,root,0755)
%if 0%{?suse_version}
%dir %{_javadocdir}
%endif
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*

%changelog
