%{?nodejs_find_provides_and_requires}

%global enable_tests 0

Name:       nodejs-uglify-to-browserify
Version:    1.0.2
Release:    2%{?dist}
Summary:    A transform to make UglifyJS work in browserify
License:    MIT
Group:      System Environment/Libraries
URL:        https://github.com/ForbesLindesay/uglify-to-browserify
Source0:    http://registry.npmjs.org/uglify-to-browserify/-/uglify-to-browserify-%{version}.tgz

BuildArch:  noarch
%if 0%{?fedora} >= 19
ExclusiveArch: %{nodejs_arches} noarch
%else
ExclusiveArch: %{ix86} x86_64 %{arm} noarch
%endif

BuildRequires:  nodejs-packaging
BuildRequires:  python

%if 0%{?enable_tests}
BuildRequires:  npm(source-map)
BuildRequires:  uglify-js
%endif

%description
%{summary}.


%prep
%setup -q -n package
for i in LICENSE README.md; do
    sed -i -e 's/\r$//' ${i}
done


%build
#nothing to do


%install
mkdir -p %{buildroot}%{nodejs_sitelib}/uglify-to-browserify
cp -pr package.json index.js \
    %{buildroot}%{nodejs_sitelib}/uglify-to-browserify

%nodejs_symlink_deps


%if 0%{?enable_tests}
%check
%nodejs_symlink_deps --check
%__nodejs test/index.js
%endif


%files
%doc LICENSE README.md
%{nodejs_sitelib}/uglify-to-browserify


%changelog
* Sat Mar 15 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1.0.2-2
- fix wrong-file-end-of-line-encoding

* Thu Mar 13 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1.0.2-1
- initial package
