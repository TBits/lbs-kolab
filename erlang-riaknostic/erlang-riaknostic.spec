%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname riaknostic
#
# This package contains only arch-independent data but install it into
# arch-dependent directory thus making this package arch-dependent. In order to
# suppress empty *-debuginfo generation we have to explicitly order
# debuginfo-generator to skip trying to build *-debuiginfo for that package.
#
%global debug_package %{nil}
%global patchnumber 0


Name:		erlang-%{realname}
Version:	2.0.1
Release:	1%{?dist}
Summary:	A diagnostic tool for Riak installations
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/riaknostic
%if 0%{?rhel} > 6 || 0%{?fedora}
VCS:		https://github.com/basho/riaknostic.git
%endif
Source0:	https://github.com/basho/riaknostic/archive/%{version}/%{realname}-%{version}.tar.gz

Patch1:     erlang-riaknostic-2.0.1-relax-deps.patch

BuildRequires:	erlang-getopt
BuildRequires:  erlang-goldrush
BuildRequires:	erlang-lager >= 2.0.3
BuildRequires:	erlang-meck
BuildRequires:	erlang-rebar
# Error:erlang(lists:keyfind/3)
Requires:	erlang-erts%{?_isa} >= R13B
Requires:	erlang-eunit%{?_isa}
Requires:	erlang-getopt%{?_isa}
Requires:	erlang-inets%{?_isa}
Requires:	erlang-kernel%{?_isa}
Requires:	erlang-lager%{?_isa}
Requires:	erlang-meck%{?_isa}
Requires:	erlang-stdlib%{?_isa}


%description
A set of tools that diagnoses common problems which could affect a Riak node or
cluster. When experiencing any problem with Riak, riaknostic should be the
first thing run during troubleshooting. The tool is a plugin for Riak which can
be used via the riak-admin script.


%prep
%setup -q -n %{realname}-%{version}
sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src
%patch1 -p1

%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv
install -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 ebin/%{realname}*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 priv/* %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv


%check
rebar eunit -v skip_deps=true


%files
%doc README.md doc/overview.edoc LICENSE
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv/
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/ForkMe_Blk.png
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/doctorbasho.jpg
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/edoc.css
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/index.html


%changelog
* Thu Jul  9 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.0.1-1
- Upgrade to version 2.0.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 01 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.1.0-1
- Initial build
