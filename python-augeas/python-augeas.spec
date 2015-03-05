#
# spec file for package python-augeas
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


Name:           python-augeas
Version:        0.4.1
Release:        0
Summary:        Python bindings for Augeas
License:        LGPL-2.1+
Group:          Development/Languages/Python

Url:            http://augeas.net/
Source:         https://fedorahosted.org/released/python-augeas/python-augeas-%{version}.tar.gz
%if 0%{?suse_version} >= 1140
BuildRequires:  augeas-lenses
%endif
BuildRequires:  python-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%if 0%{?suse_version} && 0%{?suse_version} <= 1110
%{!?python_sitelib: %global python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%else
BuildArch:      noarch
%endif

Requires:       augeas
# We'd always want to have augeas-lenses installed
%if 0%{?suse_version} >= 1140
Requires:       augeas-lenses
%endif

# Fix no-dependency-on python-base on SLE11 and openSUSE 11.4
%if 0%{?suse_version} <= 1140
%{py_requires}
%endif

%description
Python bindings for Augeas, a library for programmatically editing
configuration files.


%prep
%setup -q

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%if 0%{?suse_version} >= 1210
%check
cd test
python test_augeas.py
%endif

%files
%defattr(-,root,root)
%doc AUTHORS COPYING README.txt
%{python_sitelib}/*

%changelog
