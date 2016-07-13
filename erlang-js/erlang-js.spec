%global realname erlang_js
%global upstream basho
%{?filter_setup:
%filter_provides_in %{_libdir}/erlang/lib/.*\.so$
%filter_setup
}
%{expand: %(NIF_VER=`rpm -q erlang-erts --provides | grep --color=no erl_nif_version` ; if [ "$NIF_VER" != "" ]; then echo %%global __erlang_nif_version $NIF_VER ; fi)}
%{expand: %(DRV_VER=`rpm -q erlang-erts --provides | grep --color=no erl_drv_version` ; if [ "$DRV_VER" != "" ]; then echo %%global __erlang_drv_version $DRV_VER ; fi)}


Name:		erlang-js
Version:	1.3.0
Release:	2%{?dist}
Summary:	A Friendly Erlang to Javascript Binding
Group:		Development/Libraries
License:	ASL 2.0
URL:		http://github.com/%{upstream}/%{realname}
%if 0%{?el7}%{?fedora}
VCS:		scm:git:https://github.com/%{upstream}/%{realname}.git
%endif
Source0:	https://github.com/%{upstream}/%{realname}/archive/%{version}/%{realname}-%{version}.tar.gz

# Fedora-specific
Patch1:		erlang-js-0001-Fix-building-of-linked-in-driver.patch

# Fedora-specific
Patch2:		erlang-js-0002-build-fix-for-js-1.8.5.patch

# Fedora-specific
Patch3:		erlang-js-0003-Use-mochiweb-instead-of-a-bundled-copies.patch

# Fedora-specific
Patch4:		erlang-js-0004-Replace-deprecated-driver_output_term-with-erl_drv_o.patch

# Upstream format-patch develop/1.3.0
Patch0006:  erlang-js-0006-Fix-R18-erlang-now-deprecation-warning.patch

# From https://github.com/basho/erlang_js/pull/58
Patch58:    erlang-js-1.3.0-otp-18.3-compat.patch

BuildRequires:	erlang-rebar
BuildRequires:	erlang-rpm-macros >= 0.1.4
BuildRequires:	erlang-mochiweb
BuildRequires:	js-devel
Requires:	erlang-erts%{?_isa} >= R12B-5
Requires:	erlang-kernel%{?_isa} >= R12B-5
Requires:	erlang-mochiweb%{?_isa}
Requires:	erlang-stdlib%{?_isa} >= R12B-5
%{?__erlang_drv_version:Requires: %{__erlang_drv_version}}


%description
A Friendly Erlang to Javascript Binding.


%prep
%setup -q -n %{realname}-%{version}
%patch1 -p1 -b .bundled_libs

rm -f c_src/js-1.8.0-rc1.tar.gz
rm -f c_src/nsprpub-4.8.tar.gz

%patch2 -p1 -b .building_with_js_1_8_5
%patch3 -p1 -b .use_globally_available_mochiweb
%patch4 -p1 -b .fix_deprecated

%patch0006 -p1

%patch58 -p1

%build
rebar compile -vv


%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
mkdir -p $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/priv
install -m 644 ebin/%{realname}.app $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 ebin/*.beam $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 priv/json2.js $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/priv
install -m 755 priv/%{realname}_drv.so $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/priv


%check
rebar eunit -v


%files
%doc LICENSE README.org
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_sup.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/js.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/js_*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/json2.js
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/%{realname}_drv.so


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Nov 16 2014 Peter Lemenkov <lemenkov@gmail.com> - 1.3.0-1
- Ver. 1.3.0

* Tue Nov 04 2014 Peter Lemenkov <lemenkov@gmail.com> - 1.2.2-8
- Rebuild with Erlang 17.3.3

* Thu Aug 28 2014 Peter Lemenkov <lemenkov@gmail.com> - 1.2.2-7
- Rebuild with Erlang 17.2.1

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.2.2-5
- Use new erlang macros to build with $RPM_OPT/LD_FLAGS etc, verbosely

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Oct 25 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.2.2-3
- Rebuild with new __erlang_drv_version

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 10 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.2.2-1
- Ver. 1.2.2
- Dropped upstreamed patches

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Sep 23 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.1-2
- Fix failure during tests if built with js-1.7.0 (EL5 & EL6)

* Sat Sep 22 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.1-1
- Ver. 1.2.1
- Drop upstreamed patches

* Wed Sep 05 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.0-1
- Ver. 1.2.0

* Fri Jul 20 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.0.2-4
- Fix building releases using rebar
- Fix dependencides (add _isa)
- Drop EL5-related stuff

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 05 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.0.2-2
- Enable back building with js-1.7.0 (EL6)

* Thu Jul 05 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.0.2-1
- Ver. 1.0.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Apr 13 2011 Martin Stransky <stransky@redhat.com> - 0.5.0-3
- build fix for js 1.8.5

* Fri Jan 28 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.5.0-2
- Drop unneeded runtime dependency on eunit

* Wed Jan  5 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.5.0-1
- Ver. 0.5.0

* Fri Sep 10 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.4-1
- Initial build
