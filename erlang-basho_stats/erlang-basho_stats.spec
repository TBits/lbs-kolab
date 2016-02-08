%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname basho_stats
%global upstream basho
#
# This package contains only arch-independent data but install it into
# arch-dependent directory thus making this package arch-dependent. In order to
# suppress empty *-debuginfo generation we have to explicitly order
# debuginfo-generator to skip trying to build *-debuiginfo for that package.
#
%global debug_package %{nil}
%global git_tag 19c532a
%global patchnumber 0


Name:		erlang-%{realname}
Version:	1.0.3
Release:	5%{?dist}
Summary:	Basic Erlang statistics library
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/basho_stats
%if 0%{?rhel} > 6 || 0%{?fedora}
VCS:		https://github.com/basho/basho_stats.git
%endif
# wget --content-disposition https://github.com/basho/basho_stats/tarball/1.0.3
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz
# Fix for PowerPC (and probably for other BigEndian arches) FPU
Patch1:		erlang-basho_stats-0001-Fix-for-PowerPC.patch
BuildRequires:	erlang-rebar
# Error:erlang(erlang:max/2)
# Error:erlang(erlang:min/2)
Requires:	erlang-erts%{?_isa} >= R13B
Requires:	erlang-stdlib%{?_isa}


%description
Basic Erlang statistics library.


%prep
%setup -q -n %{upstream}-%{realname}-65e2373
#ifarch ppc %{power64}
#patch1 -p1 -b .bigendian
#endif


%build
rebar compile -v


%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,include}
install -p -m 644 ebin/%{realname}.app $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 644 ebin/*.beam $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 644 include/*.hrl $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/include


%check
rebar eunit skip_deps=true -v


%files
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include/
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/*.hrl


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 01 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.0.3-2
- Disable fix for mysterious ppc-related issue (can't reproduce in Koji)

* Sun Mar 10 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.0.3-1
- Ver. 1.0.3 (just a version bump - no more changes)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 16 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.0.2-1
- Ver. 1.0.2

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Feb 25 2011 Peter Lemenkov <lemenkov@gmail.com> - 1.0.1-1
- Initial package
