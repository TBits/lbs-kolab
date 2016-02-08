%global realname sidejob
#
# This package contains only arch-independent data but install it into
# arch-dependent directory thus making this package arch-dependent. In order to
# suppress empty *-debuginfo generation we have to explicitly order
# debuginfo-generator to skip trying to build *-debuiginfo for that package.
#
%global debug_package %{nil}
%global patchnumber 0


Name:		erlang-%{realname}
Version:	0.2.0
Release:	5%{?dist}
Summary:	An Erlang library that implements a parallel, capacity-limited request pool
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/sidejob
%if 0%{?rhel} > 6 || 0%{?fedora}
VCS:		https://github.com/basho/sidejob.git
%endif
Source0:	https://github.com/basho/sidejob/archive/%{version}/%{realname}-%{version}.tar.gz
BuildRequires:	erlang-rebar
Requires:	erlang-compiler%{?_isa}
# Error:erlang(erlang:atom_to_binary/2)
# Error:erlang(erlang:binary_to_atom/2)
# Error:erlang(erlang:max/2)
Requires:	erlang-erts%{?_isa} >= R13B
Requires:	erlang-kernel%{?_isa}
Requires:	erlang-stdlib%{?_isa}
Requires:	erlang-syntax_tools%{?_isa}


%description
An Erlang library that implements a parallel, capacity-limited request pool. In
sidejob, these pools are called resources. A resource is managed by multiple
gen_server like processes which can be sent calls and casts using sidejob:call
or sidejob:cast respectively.


%prep
%setup -q -n %{realname}-%{version}


%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 ebin/%{realname}*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin


%check
# Requires a proprietary test-site, QuickCheck
#rebar eunit -v


%files
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}*.beam


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Aug 06 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.2.0-2
- Remove useless empty README.md
- Fixed rpmlint warning about wrong Source0

* Wed Jul 31 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.2.0-1
- Initial build
