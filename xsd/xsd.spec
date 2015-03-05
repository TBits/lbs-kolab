#
# spec file for package xsd
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
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

Name:           xsd
%define rversion 3.3.0-1
Version:        3.3.0.1
Release:        0
Summary:        W3C XML schema to C++ data binding compiler
# http://www.codesynthesis.com/products/xsd/license.xhtml
License:        SUSE-GPL-2.0-with-FLOSS-exception
Url:            http://www.codesynthesis.com/products/xsd/
Group:          Development/Languages/C and C++
Source0:        http://www.codesynthesis.com/download/xsd/3.3/%{name}-%{rversion}+dep.tar.bz2
# Rename xsd to xsdcxx
Patch0:         xsdcxx-rename.patch
# Author: Konstantinos Margaritis <markos@genesi-usa.com> - http://bugs.debian.org/624942
Patch1:         boost1.46-buildfix.patch

%if 0%{?suse_version}
BuildRequires:  Xerces-c-devel
%else
BuildRequires:  xerces-c-devel
%endif

BuildRequires:  boost-devel
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  m4

%if 0%{?suse_version}
Requires:       Xerces-c-devel
%else
Requires:       xerces-c-devel
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
CodeSynthesis XSD is an open-source, cross-platform W3C XML Schema to
C++ data binding compiler. Provided with an XML instance specification
(XML Schema), it generates C++ classes that represent the given
vocabulary as well as parsing and serialization code.
You can then access the data stored in XML using types and functions
that semantically correspond to your application domain rather than
dealing with intricacies of reading and writing XML.

%package        doc
Summary:        API documentation files for xsd
Requires:       xsd
Group:          Documentation/Other

%description    doc
This package contains API documentation for xsd.

%prep
%setup -q -n %{name}-%{rversion}+dep
%patch0 -p1
%patch1 -p1

%build
make verbose=1 CXXFLAGS="%{optflags}" %{?_smp_mflags}

%install
make install_prefix="%{buildroot}%{_prefix}"  install

# Rename xsd to xsdcxx to avoid conflicting with mono-web package.
mv %{buildroot}%{_bindir}/xsd %{buildroot}%{_bindir}/xsdcxx
mv %{buildroot}%{_datadir}/doc/xsd %{buildroot}%{_datadir}/doc/xsdcxx
mv %{buildroot}%{_mandir}/man1/xsd.1 %{buildroot}%{_mandir}/man1/xsdcxx.1

# Remove duplicate docs.
rm -rf %{buildroot}%{_datadir}/doc/libxsd

# Remove Microsoft Visual C++ compiler helper files.
rm -rf %{buildroot}%{_includedir}/xsd/cxx/compilers

%fdupes -s %{buildroot}%{_datadir}/doc

%files
%defattr(-,root,root,-)
%doc README xsd/NEWS xsd/LICENSE xsd/GPLv2 xsd/FLOSSE
%{_bindir}/xsdcxx
%{_includedir}/xsd/
%{_mandir}/man1/xsdcxx.1*

%files doc
%defattr(-,root,root,-)
%doc %{_datadir}/doc/xsdcxx

%changelog
