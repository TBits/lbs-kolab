%{?nodejs_find_provides_and_requires}

#enable/disable tests in case the deps aren't there
%global enable_tests 1

%if 0%{?fedora}
%global installdir  %{_jsdir}
%else
%global installdir  %{_datadir}/javascript
%endif

Name:           uglify-js
Version:        2.4.13
Release:        5%{?dist}
Summary:        JavaScript parser, mangler/compressor and beautifier toolkit
BuildArch:      noarch

Group:          Development/Tools
#no license file included; BSD license in source header
License:        BSD
URL:            https://github.com/mishoo/UglifyJS2
Source0:        http://registry.npmjs.org/uglify-js/-/uglify-js-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:  noarch
%if 0%{?fedora} >= 19
ExclusiveArch: %{nodejs_arches} noarch
%else
ExclusiveArch: %{ix86} x86_64 %{arm} noarch
%endif

Provides:       nodejs-uglify-js = %{version}-%{release}

BuildRequires:  nodejs-packaging
BuildRequires:  python

%if 0%{?fedora}
BuildRequires:  web-assets-devel
%endif

%if 0%{?enable_tests}
BuildRequires:  npm(async)
BuildRequires:  npm(optimist)
BuildRequires:  npm(source-map)
%endif

Requires: js-uglify = %{version}-%{release}

%description
JavaScript parser, mangler/compressor and beautifier toolkit.

This package ships the uglifyjs command-line tool and a library suitable for
use within Node.js.

%package -n js-uglify
Summary: JavaScript parser, mangler/compressor and beautifier toolkit - core library
Group: System Environment/Libraries

Obsoletes: uglify-js-common < 2.2.5-4
Provides: uglify-js-common = %{version}-%{release}

%if 0%{?fedora}
Requires: web-assets-filesystem
%endif

%description -n js-uglify
JavaScript parser, mangler/compressor and beautifier toolkit.

This package ships a JavaScript library suitable for use by any JavaScript
runtime.

%prep
%setup -q -n package

%nodejs_fixdep optimist 0.4.x

%build
#nothing to do

%install
rm -rf %buildroot

mkdir -p %{buildroot}%{installdir}/%{name}-2
cp -pr lib/* %{buildroot}%{installdir}/%{name}-2
ln -sf %{name}-2 %{buildroot}%{installdir}/%{name}

#compat symlink
mkdir -p %{buildroot}%{_datadir}
ln -sf javascript/%{name} %{buildroot}%{_datadir}/%{name}

mkdir -p %{buildroot}%{nodejs_sitelib}/uglify-js@2
cp -pr bin tools package.json %{buildroot}%{nodejs_sitelib}/uglify-js@2
ln -sf %{installdir}/%{name} %{buildroot}%{nodejs_sitelib}/uglify-js@2/lib

mkdir -p %{buildroot}%{_bindir}
ln -sf ../lib/node_modules/uglify-js@2/bin/uglifyjs %{buildroot}%{_bindir}/uglifyjs

%nodejs_symlink_deps

ln -sf uglify-js@2 %{buildroot}%{nodejs_sitelib}/uglify-js

%if 0%{?enable_tests}
%check
%nodejs_symlink_deps --check
%__nodejs test/run-tests.js
%endif

%clean
rm -rf %buildroot

%pretrans -p <lua>
st = posix.stat("%{nodejs_sitelib}/uglify-js")
if st and st.type == "directory" then
  os.execute("rm -rf %{nodejs_sitelib}/uglify-js")
end

%pretrans -n js-uglify -p <lua>
st = posix.stat("%{_datadir}/%{name}")
if st and st.type == "directory" then
  os.execute("rm -rf %{_datadir}/%{name}")
end

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/uglify-js
%{nodejs_sitelib}/uglify-js@2
%{_bindir}/uglifyjs

%files -n js-uglify
%defattr(-,root,root,-)
%{installdir}/%{name}-2
%{installdir}/%{name}
%{_datadir}/%{name}
%doc LICENSE README.md


%changelog
* Thu May 08 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 2.4.13-5
- add logic for building on EL6

* Tue Apr 29 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 2.4.13-4
- pretrans script should actually be split in two, so one half should run in
  uglify-js and the other half should run in js-uglify (#1092184)

* Tue Apr 01 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 2.4.13-3
- pretrans script should run in js-uglify subpackage (#1082946)

* Sat Mar 15 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 2.4.13-2
- add logic for building on EPEL 6 as web-assets-{devel,filesystem} are not
  yet available

* Thu Mar 13 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 2.4.13-1
- update to upstream release 2.4.13

* Mon Jan 20 2014 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.5-4
- port to new JS guidelines
- provide the nodejs- form

* Sun Jan 19 2014 Tom Hughes <tom@compton.nu> - 2.2.5-3
- use new multi-version packaging rules
- update to latest nodejs packaging standards

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 16 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.5-1
- new upstream release 2.2.5

* Tue Apr 16 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.4-3
- call nodejs_symlink_deps
- fix optimist dep for 0.4.0

* Wed Feb 13 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.4-2
- install tools dir
- enable tests

* Wed Feb 13 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.4-1
- new upstream release 2.2.4

* Fri Feb 01 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.3-6
- rearrange symlinks so dep generator works

* Fri Feb 01 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.3-5
- really fix install section
- conditionalize tests

* Thu Jan 31 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.3-4
- fix install section

* Thu Jan 31 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.3-3
- split off -common subpackage for use with other runtimes

* Fri Jan 18 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.3-2
- BuildRequire deps so tests work

* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.3-1
- initial package generated by npm2rpm
