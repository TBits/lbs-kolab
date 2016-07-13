%if 0%{?fedora} < 13 && 0%{?rhel} < 6
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

Name:           python-riak
Version:        2.5.4
Release:        1%{?dist}
Summary:        Python client library for Riak

Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/basho/riak-python-client
Source0:        http://pypi.python.org/packages/source/r/riak/riak-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
%if 0%{?suse_version}
BuildRequires:  python-devel
%else
BuildRequires:  python2-devel
%endif
BuildRequires:  python-setuptools

Requires:       pyOpenSSL >= 0.14
Requires:       python-riak_pb

%description
Python client for Riak

%prep
%setup -q -n riak-%{version}

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
%{python_sitelib}/riak
%{python_sitelib}/*.egg-info

%changelog
* Fri Dec  5 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.1.0-1
- First package
