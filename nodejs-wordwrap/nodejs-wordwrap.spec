%{?nodejs_find_provides_and_requires}

%global enable_tests 1

Name:           nodejs-wordwrap
Version:        0.0.2
Release:        4%{?dist}
Summary:        Word wrapping library for node

Group:          System Environment/Libraries
#no license file included; "MIT/X11" indicated in package.json
License:        MIT
URL:            https://github.com/substack/node-wordwrap
Source0:        http://registry.npmjs.org/wordwrap/-/wordwrap-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:  noarch
%if 0%{?fedora} >= 19
ExclusiveArch: %{nodejs_arches} noarch
%else
ExclusiveArch: %{ix86} x86_64 %{arm} noarch
%endif

BuildRequires:  nodejs-packaging
BuildRequires:  python

%if 0%{?enable_tests}
BuildRequires:  npm(expresso)
%endif

%description
Wrap those words. Show them at what columns to start and stop.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %buildroot
mkdir -p %{buildroot}%{nodejs_sitelib}/wordwrap
cp -pr package.json index.js %{buildroot}%{nodejs_sitelib}/wordwrap

%nodejs_symlink_deps

%if 0%{?enable_tests}
%check
%nodejs_symlink_deps --check
ln -sf .. node_modules/wordwrap
expresso
%endif

%clean
rm -rf %buildroot

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/wordwrap
%doc README.markdown example

%changelog
* Tue Aug 20 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.0.2-4
- restrict to compatible arches
- enable tests

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.2-2
- fix License tag

* Fri Jan 18 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.2-1
- initial package generated by npm2rpm