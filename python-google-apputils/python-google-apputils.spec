%if 0%{?fedora} < 13 && 0%{?rhel} < 6
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

Name:           python-google-apputils
Version:        0.4.1
Release:        1.27%{?dist}.kolab_wf
Summary:        Google Application Utilities for Python

Group:          Development/Libraries
License:        ASL 2.0
URL:            https://code.google.com/p/google-apputils-python/
Source0:        https://google-apputils-python.googlecode.com/files/google-apputils-%{version}.tar.gz

Patch0:         python-google-apputils-0.4.1-no-ez_setup.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
%if 0%{?suse_version}
BuildRequires:	python-devel
%else
BuildRequires:  python2-devel
%endif
BuildRequires:	python-setuptools

%description
Python client for Riak

%prep
%setup -q -n google-apputils-%{version}

%patch0 -p1

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --prefix=%{_prefix} --root $RPM_BUILD_ROOT

%check

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{python_sitelib}/google
%{python_sitelib}/google/apputils
%{python_sitelib}/*.egg-info
%{python_sitelib}/*.pth

%changelog
* Fri Dec  5 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.4.1-1
- First package
