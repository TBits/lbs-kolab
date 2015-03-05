%{?nodejs_find_provides_and_requires}

%global enable_tests 1

Name:       expresso
Version:    0.9.2
Release:    5%{?dist}
Summary:    A lightweight, fast, test-driven development (TDD) framework for Node.js
License:    MIT
Group:      System Environment/Libraries
URL:        https://github.com/visionmedia/expresso
Source0:    http://registry.npmjs.org/expresso/-/expresso-%{version}.tgz
Source1:    expresso.1

BuildArch:  noarch
%if 0%{?fedora} >= 19
ExclusiveArch: %{nodejs_arches} noarch
%else
ExclusiveArch: %{ix86} x86_64 %{arm} noarch
%endif

BuildRequires:  nodejs-packaging
BuildRequires:  python

%description
%{summary}.


%prep
%setup -q -n package
rm -rf deps/


%build
#nothing to do


%install
mkdir -p %{buildroot}%{nodejs_sitelib}/expresso
cp -pr package.json \
    %{buildroot}%{nodejs_sitelib}/expresso
mkdir -p %{buildroot}{%nodejs_sitelib}/expresso/bin
install -p -D -m0755 bin/expresso \
    %{buildroot}%{nodejs_sitelib}/expresso/bin/expresso
mkdir -p %{buildroot}%{_bindir}
ln -s %{nodejs_sitelib}/expresso/bin/expresso %{buildroot}/%{_bindir}/expresso

mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m0644 %{SOURCE1} \
    %{buildroot}%{_mandir}/man1/expresso.1

%nodejs_symlink_deps


%if 0%{?enable_tests}
%check
rm -f test/bar.test.js
rm -f test/foo.test.js
bin/expresso --growl
bin/expresso -I lib --cov
bin/expresso --serial test/serial/*.test.js
%endif


%files
%doc History.md Readme.md docs/
%{nodejs_sitelib}/expresso
%{_bindir}/expresso
%{_mandir}/man1/expresso.1*


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 27 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.9.2-4
- restrict to compatible arches

* Sun Feb 24 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.9.2-3
- make sure bundled jscoverage is purged
- add man page

* Thu Feb 14 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.9.2-2
- rename from nodejs-expresso to just expresso

* Thu Feb 14 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.9.2-1
- initial package
