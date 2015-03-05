%if 0%{?opensuse_bs}
#!BuildIgnore:  python-jinja2-26
%endif

%global mod_name	Flask-Babel

Name:		python-flask-babel
Version:	0.9
Release:	1%{?dist}
Summary:	Adds i18n/l10n support to Flask applications
Group:		Development/Libraries
License:	BSD
URL:		http://github.com/mitsuhiko/flask-babel/
Source0:	http://pypi.python.org/packages/source/F/%{mod_name}/%{mod_name}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python-babel
BuildRequires:	python-devel
BuildRequires:	python-flask
BuildRequires:  python-jinja2
BuildRequires:	python-setuptools
BuildRequires:	python-speaklater
BuildRequires:	pytz
Requires:	python-babel
Requires:	python-flask
Requires:	python-speaklater
Requires:	pytz

%description
Adds i18n/l10n support to Flask applications with the help of the Babel library.

%prep
%setup -q -n %{mod_name}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --root $RPM_BUILD_ROOT

%check
PYTHONPATH=$RPM_BUILD_ROOT/%{python_sitelib}:%{python_sitelib} make test || :

%files
%doc docs LICENSE PKG-INFO README
%{python_sitelib}/*.egg-info/
%{python_sitelib}/flask_babel/*.py*

%changelog
* Fri Jul 18 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.9-1
- Update to latest upstream release (#1106770).

* Thu Jul 17 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.8-6
- Add patch to work with latest Babel (#1106770).

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 13 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.8-4
- Add missing python-setuptools build requires (#839071)
- Remove wrongly installed .gitignore

* Fri Aug 17 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.8-3
- Add missing build requires for proper chroot build
- Correct spec file to make %%check work without having package installed

* Sun Aug 5 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.8-2
- No need to set CFLAGS for noarch (#839071)
- Add %%check section (#839071)

* Tue Jul 10 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.8-1
- Initial python-flask-babel spec.
