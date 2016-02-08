%global pypi_name cssmin

%if 0%{?rhel} > 7
%global with_python3 1
%endif

Name:       python-cssmin
Version:    0.2.0
Release:    1%{?dist}
Summary:    A Python port of the YUI CSS compression algorithm

Group:      Development/Libraries
License:    BSD
URL:        http://github.com/zacharyvoase/cssmin
Source0:    https://pypi.python.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Patch0:     python-distutils.patch

BuildArch:  noarch
Requires:   python-setuptools
%if 0%{?suse_version}
BuildRequires:  python-devel python-setuptools
%else
BuildRequires:  python2-devel python-setuptools
%if 0%{?with_python3}
Requires:   python3-setuptools
BuildRequires:  python3-devel python3-setuptools
%endif
%endif

%description
A Python port of the YUI CSS compression algorithm. The library can be used for
merging and compressing CSS files.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary: %{summary}


%description -n python3-%{pypi_name}
%{description}

This is the version for Python 3.x.
%endif

%prep
%setup -q -n %{pypi_name}-%{version}
%patch0 -p1

# remove shebang from non-executable
sed '1{\@^#!/usr/bin/env python@d}' src/cssmin.py > src/cssmin.py.new &&
touch -r  src/cssmin.py src/cssmin.py.new &&
mv src/cssmin.py.new src/cssmin.py

sed -i 's/^from distribute_setup/#/' setup.py

%build
%{__python} setup.py build


%install
%if 0%{?with_python3}
# install py3 version first, so that binary gets overwritten by py2 version
%{__python3} setup.py install --skip-build -O1 --root %{buildroot}
%endif
%{__python} setup.py install --skip-build -O1 --root %{buildroot}

mv %{buildroot}%{_bindir}/cssmin.py %{buildroot}%{_bindir}/python-cssmin

%check
cd src && \
%{__python} -c 'import cssmin; cssmin.cssmin("""\
#href { \
  font-size: 3; \
}""")'; \

%if 0%{?with_python3}
cd src && \
%{__python3} -c 'import cssmin; cssmin.cssmin("""\
#href { \
  font-size: 3; \
}""")'; \
%endif

%files
%doc PKG-INFO
%{python_sitelib}/cssmin.py*
%{python_sitelib}/*.egg-info
%{_bindir}/*


%if 0%{?with_python3}
%files -n python3-cssmin
%{python3_sitelib}/cssmin.py
%{python3_sitelib}/__pycache__/cssmin.*.py*
%{python3_sitelib}/*.egg-info
%endif


%changelog
* Mon Feb 10 2014 Martin Krizek <mkrizek@redhat.com> - 0.2.0-1
- Update to 0.2.0
- Add setuptools as requires
- Rename /usr/bin/cssmin (#1048622)

* Tue Oct 15 2013 Martin Krizek <mkrizek@redhat.com> - 0.1.4-6
- Fix building on f20 and higher

* Wed Oct 09 2013 Martin Krizek <mkrizek@redhat.com> - 0.1.4-5
- Add python3-setuptools as BuildRequires

* Tue Oct 08 2013 Martin Krizek <mkrizek@redhat.com> - 0.1.4-4
- Describe the package in more detail

* Mon Oct 07 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.1.4-3
- Add python3 subpackage and modify %%check section

* Mon Oct 07 2013 Martin Krizek <mkrizek@redhat.com> - 0.1.4-2
- Add python3-devel as dep
- Add check section

* Tue Oct 01 2013 Martin Krizek <mkrizek@redhat.com> - 0.1.4-1
- Initial packaging
