%global realname pybeam
%global upstream matwey
%global debug_package %{nil}

%if 0%{?rhel}
%global with_python3 0
%endif

%{!?python2_sitelib: %define python2_sitelib %{python_sitelib}}

Name:		python-%{realname}
Version:	0.3.2
Release:	1.28%{?dist}.kolab_16
Summary:	Python module to parse Erlang BEAM files
License:	MIT
Group:		Development/Languages
URL:		https://github.com/%{upstream}/%{realname}
%if 0%{?el7}%{?fedora}
VCS:		scm:git:https://github.com/%{upstream}/%{realname}.git
%endif
Source0:	https://github.com/%{upstream}/%{realname}/archive/%{version}/%{realname}-%{version}.tar.gz

Patch1:     pybeam-0.3.2-python26.patch

BuildArch:	noarch


%description
Python module to parse Erlang BEAM files.


%package -n python2-%{realname}
Summary:	%{summary}
BuildRequires:	python-construct
BuildRequires:	python-devel
BuildRequires:	python-setuptools
Requires:	python-construct
Requires:	python-six >= 1.4.0
Provides:	python-%{realname} = %{version}-%{release}

%description -n python2-%{realname}
Python module to parse Erlang BEAM files.

%if 0%{?with_python3}
%package -n python3-%{realname}
Summary:	%{summary}
BuildRequires:	python3-construct
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
Requires:	python3-construct
Requires:	python3-six >= 1.4.0


%description -n python3-%{realname}
Python module to parse Erlang BEAM files.
%endif

%prep
%setup -q -n %{realname}-%{version}

%if 0%{?rhel} < 7
%patch1 -p1
%endif

%build
%if 0%{?fedora}
%py2_build
%else
python setup.py build
%endif
%if 0%{?with_python3}
%py3_build
%endif

%install
# Must do the python2 install first because the scripts in /usr/bin are
# overwritten with every setup.py install, and in general we want the
# python3 version to be the default.
%if 0%{?fedora}
%py2_install
%else
python setup.py install -O1 --skip-build --root %{buildroot}
%endif
%if 0%{?with_python3}
%py3_install
%endif

%check
%if 0%{?fedora}
%{__python2} setup.py test
%else
python setup.py test
%endif
%if 0%{?with_python3}
%{__python3} setup.py test
%endif

%files -n python2-%{realname}
%if 0%{?fedora}
%license LICENSE
%else
%doc LICENSE
%endif
%doc README.md
%{python2_sitelib}/*


%if 0%{?with_python3}
%files -n python3-%{realname}
%if 0%{?fedora}
%license LICENSE
%else
%doc LICENSE
%endif
%doc README.md
%{python3_sitelib}/*
%endif

%changelog
* Mon Feb 15 2016 Peter Lemenkov <lemenkov@gmail.com> - 0.3.2-1
- Initial build
