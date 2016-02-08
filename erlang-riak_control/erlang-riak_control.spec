%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname riak_control
%global upstream basho
#
# This package contains only arch-independent data but install it into
# arch-dependent directory thus making this package arch-dependent. In order to
# suppress empty *-debuginfo generation we have to explicitly order
# debuginfo-generator to skip trying to build *-debuiginfo for that package.
#
%global debug_package %{nil}
%global git_tag 5898c40
%global patchnumber 0


Name:		erlang-%{realname}
Version:	2.1.1
Release:	1%{?dist}
Summary:	Admin UI for Riak
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/riak_control
%if 0%{?rhel} > 6 || 0%{?fedora}
VCS:		https://github.com/basho/riak_control.git
%endif
# wget --content-disposition https://github.com/basho/riak_control/tarball/2.1.1
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz
# Fedora/EPEL-specific - will be proposed for upstream.
Patch1:		erlang-riak_control-0001-Fix-includes.patch
Patch2:		erlang-riak_control-0002-Fix-webmachine-dep.patch
Patch3:		erlang-riak_control-0003-Fix-version-in-app-file.patch
BuildRequires:	erlang-erlydtl >= 0.7.0
BuildRequires:	erlang-rebar
BuildRequires:	erlang-riak_core >= 2.1.1
BuildRequires:	erlang-webmachine >= 1.9.3
Requires:	erlang-crypto%{?_isa}
Requires:	erlang-erlydtl%{?_isa} >= 0.7.0
# Error:erlang(binary:replace/4)
# Error:erlang(erlang:max/2) in R12B and below
# Error:erlang(erlang:min/2) in R12B and below
# Error:erlang(lists:keyfind/3) in R12B and below
Requires:	erlang-erts%{?_isa} >= R13B
Requires:	erlang-kernel%{?_isa}
Requires:	erlang-mochiweb%{?_isa}
Requires:	erlang-os_mon%{?_isa}
# Error:erlang(rebar_js_uglifier_plugin:compress/3)
Requires:	erlang-rebar%{?_isa}
Requires:	erlang-riak_core%{?_isa} >= 2.1.1
Requires:	erlang-stdlib%{?_isa}
Requires:	erlang-webmachine%{?_isa} >= 1.9.3


%description
Riak Control is a set of webmachine resources, all accessible via the
/admin/* paths, allow you to inspect your running cluster, and manipulate
it in various ways.


%prep
%setup -q -n %{upstream}-%{realname}-4c2a98c
sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src
chmod 644 priv/admin/fonts/*
#%patch1 -p1 -b .includes
%patch2 -p1 -b .wm_ver
#%patch3 -p1 -b .fix_ver
# remove bundled rebar copy - just to be absolutely sure
rm -f ./rebar


%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,include,priv}
install -p -m 0644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -p -m 0644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 0644 include/%{realname}.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include/
cp -arv priv/* %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv


%check
# Some tests requires a proprietary library - QuickCheck
rebar eunit skip_deps=true -v || :


%files
%doc LICENSE README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv/
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/%{realname}.hrl
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/*


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 01 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.2-3
- Actually fix version mismatch

* Wed Jul 31 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.2-2
- Fix version mismatch

* Wed Jul 03 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.2-1
- Ver. 1.3.2

* Sun Mar 24 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.1-1
- Ver. 1.3.1

* Tue Mar 12 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.0-1
- Ver. 1.3.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Nov 18 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.1-2
- Fixed HTTPS-only access

* Fri Oct 19 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.1-1
- Ver. 1.2.1

* Thu Jul 26 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.1.2-2
- Fixed mixed macro usage in spec (mostly cosmetic change)
- Dropped remaining stuff required by EL5

* Thu May 17 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.1.2-1
- Initial package
