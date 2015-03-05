%if 0%{?opensuse_bs}
#!BuildIgnore:  python-jinja2-26
%endif

%global mod_name Flask-SQLAlchemy

%if 0%{?fedora} > 12
%global with_python3 1
%endif

Name:           python-flask-sqlalchemy
Version:        1.0
Release:        4%{?dist}
Summary:        Adds SQLAlchemy support to Flask application

Group:          Development/Libraries
License:        BSD
URL:            http://github.com/mitsuhiko/flask-sqlalchemy
Source0:        http://pypi.python.org/packages/source/F/%{mod_name}/%{mod_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-flask
Requires:       python-sqlalchemy >= 0.8

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-flask
%endif

%description
Flask-SQLAlchemy is an extension for Flask that adds support for
SQLAlchemy to your application. It aims to simplify using SQLAlchemy with 
Flask by providing useful defaults and extra helpers that make it easier 
to accomplish common tasks.

%if 0%{?with_python3}
%package -n python3-flask-sqlalchemy
Summary:        Adds SQLAlchemy support to Flask application
Group:          Development/Libraries
Requires:       python3-sqlalchemy

%description -n python3-flask-sqlalchemy
Flask-SQLAlchemy is an extension for Flask that adds support for
SQLAlchemy to your application. It aims to simplify using SQLAlchemy with 
Flask by providing useful defaults and extra helpers that make it easier 
to accomplish common tasks.

This package includes the python 3 version of the module.
%endif # with_python3

%prep
%setup -q -n %{mod_name}-%{version}
rm -f docs/_static/.DS_Store
rm -f docs/.DS_Store
rm -f docs/_themes/.gitignore
chmod -x docs/_static/flask-sqlalchemy-small.png

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
%doc docs/ README CHANGES LICENSE PKG-INFO
%{python_sitelib}/*.egg-info/
%{python_sitelib}/flask_sqlalchemy/*

%if 0%{?with_python3}
%files -n python3-flask-sqlalchemy
%doc docs/ README CHANGES LICENSE PKG-INFO
%{python3_sitelib}/*.egg-info/
%{python3_sitelib}/flask_sqlalchemy/*
%endif # with_python3

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Jan 21 2014 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 1.0-2
- Fixed #1055251

* Wed Aug 07 2013 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 1.0-1
- Upgraded to upstream 1.0 and added python3 support

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 09 2012 Tim Flink <tflink@fedoraproject.ort> - 0.16-1
- Upgraded to upstream 0.16

* Tue Aug 21 2012 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 0.14-4
- Added python-sqlalchemy as requires

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 0.14-1
- Initial RPM release
