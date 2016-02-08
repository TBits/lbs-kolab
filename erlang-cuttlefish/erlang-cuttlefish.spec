%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname cuttlefish
%global upstream basho
%global debug_package %{nil}
%global git_tag 1f82923
%global patchnumber 0


Name:		erlang-%{realname}
Version:	2.0.3
Release:	1%{?dist}
Summary:	Distributed systems infrastructure used by Riak
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/riak_core
# wget --content-disposition https://github.com/basho/riak_core/tarball/1.3.2
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz

Patch1:     erlang-cuttlefish-2.0.3-relax-lager-dep.patch
Patch2:     erlang-cuttlefish-2.0.3-set-version-number.patch

# Required for unit-tests only (if you're not interested in a compile-time
# testing then you may remove these lines):
BuildRequires:	erlang-getopt >= 0.4.3
BuildRequires:  erlang-goldrush >= 0.1.6
BuildRequires:	erlang-lager >= 2.0.3
BuildRequires:	erlang-neotoma >= 1.7.2

# Compile-time requirements
BuildRequires:	erlang-meck >= 0.7.2
BuildRequires:	erlang-rebar

Requires:   erlang-goldrush%{?_isa}
# Error:erlang(dtrace:put_utag/1)
Requires:	erlang-getopt%{?_isa}
Requires:	erlang-lager%{?_isa}
Requires:	erlang-neotoma%{?_isa}


%description
Distributed systems infrastructure used by Riak.


%prep
%setup -q -n %{upstream}-%{realname}-f3645f6
%patch1 -p1
%patch2 -p1

%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 0755 %{realname} %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,priv}
install -p -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
cp -a priv/* %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/.


%check
rebar eunit skip_deps=true -v || :


%files
%doc README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_bindir}/%{realname}
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/priv


%changelog
* Wed Jul  8 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.0.3-1
- Initial package
