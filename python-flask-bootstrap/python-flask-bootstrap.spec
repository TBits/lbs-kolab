%if 0%{?opensuse_bs}
#!BuildIgnore:  python-jinja2-26
%endif

%global mod_name Flask-Bootstrap
%if 0%{?fedora} > 18
%global with_python3 1
%endif

Name:           python-flask-bootstrap
Version:        3.2.0.2
Release:        1.26%{?dist}.kolab_wf
Summary:        Adds the Bootstrap extension to Flask applications

Group:          Development/Libraries
License:        BSD
URL:            http://pythonhosted.org/Flask-Bootstrap/
Source0:        http://pypi.python.org/packages/source/F/%{mod_name}/%{mod_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-flask
Requires:       python-flask

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-flask
%endif

%description
Flask-Bootstrap packages Bootstrap into an extension that mostly
consists of a blueprint named 'bootstrap'. It can also create
links to serve Bootstrap from a CDN and works with no boilerplate
code in your application.

%if 0%{?with_python3}
%package -n python3-flask-bootstrap
Summary:        Adds the Bootstrap extension to Flask applications
Group:          Development/Libraries
Requires:       python3-sqlalchemy

%description -n python3-flask-bootstrap
Flask-Bootstrap packages Bootstrap into an extension that mostly
consists of a blueprint named 'bootstrap'. It can also create
links to serve Bootstrap from a CDN and works with no boilerplate
code in your application.

This package includes the python 3 version of the module.
%endif # with_python3

%prep
%setup -q -n %{mod_name}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
mkdir -p $RPM_BUILD_ROOT%{python3_sitelib}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif
 
%files
%{python_sitelib}/*.egg-info
%dir %{python_sitelib}/flask_bootstrap
%{python_sitelib}/flask_bootstrap/*

%if 0%{?with_python3}
%files -n python3-flask-bootstrap
%doc docs/ README CHANGES LICENSE PKG-INFO
%{python3_sitelib}/*.egg-info
%dir %{python3_sitelib}/flask_bootstrap
%{python3_sitelib}/flask_bootstrap/*
%endif # with_python3

%changelog
* Mon Oct 13 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 3.2.0.2-1
- First package
