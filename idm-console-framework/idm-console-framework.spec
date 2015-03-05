#
# spec file for package idm-console-framework
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


Name:           idm-console-framework
Version:        1.1.7
Release:        0
Summary:        Identity Management Console Framework
Group:          System/Libraries
License:        LGPL-2.0
URL:            http://port389.org

Source:         http://port389.org/sources/%name-%version.tar.bz2
BuildRoot:      %_tmppath/%name-%version-build
BuildArch:      noarch
BuildRequires:  ant >= 1.6.2
BuildRequires:  java-devel >= 1.6.0
BuildRequires:  ldapjdk
BuildRequires:  mozilla-jss >= 4.2
# Urge use of OpenJDK for runtime
Requires:       java >= 1.6.0
Requires:       ldapjdk
Requires:       mozilla-jss >= 4.2

%global majorrel 1.1

%description
A Java Management Console framework used for remote server management.

%prep
%setup -q

%build
%ant \
    -Dlib.dir=%_libdir \
    -Djss.local.location=%_libdir/java \
    -Dbuilt.dir=`pwd`/built \
    -Dclassdest=%_javadir 

%install
export NO_BRP_CHECK_BYTECODE_VERSION=true
install -d %buildroot%_javadir
install -m644 built/release/jars/idm-console-* %buildroot%_javadir

# create symlinks
pushd %buildroot%_javadir
ln -s idm-console-base-%version.jar idm-console-base-%majorrel.jar
ln -s idm-console-base-%version.jar idm-console-base.jar
ln -s idm-console-mcc-%version.jar idm-console-mcc-%majorrel.jar
ln -s idm-console-mcc-%version.jar idm-console-mcc.jar
ln -s idm-console-mcc-%{version}_en.jar idm-console-mcc-%{majorrel}_en.jar
ln -s idm-console-mcc-%{version}_en.jar idm-console-mcc_en.jar
ln -s idm-console-nmclf-%version.jar idm-console-nmclf-%majorrel.jar
ln -s idm-console-nmclf-%version.jar idm-console-nmclf.jar
ln -s idm-console-nmclf-%{version}_en.jar idm-console-nmclf-%{majorrel}_en.jar
ln -s idm-console-nmclf-%{version}_en.jar idm-console-nmclf_en.jar
popd

%files
%defattr(-,root,root)
%doc LICENSE
%_javadir/idm-console-base-%version.jar
%_javadir/idm-console-base-%majorrel.jar
%_javadir/idm-console-base.jar
%_javadir/idm-console-mcc-%version.jar
%_javadir/idm-console-mcc-%majorrel.jar
%_javadir/idm-console-mcc.jar
%_javadir/idm-console-mcc-%{version}_en.jar
%_javadir/idm-console-mcc-%{majorrel}_en.jar
%_javadir/idm-console-mcc_en.jar
%_javadir/idm-console-nmclf-%version.jar
%_javadir/idm-console-nmclf-%majorrel.jar
%_javadir/idm-console-nmclf.jar
%_javadir/idm-console-nmclf-%{version}_en.jar
%_javadir/idm-console-nmclf-%{majorrel}_en.jar
%_javadir/idm-console-nmclf_en.jar

%changelog
