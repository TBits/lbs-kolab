%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname lager_syslog
%global upstream basho
%global debug_package %{nil}
%global git_tag fa2e7e3
%global patchnumber 0


Name:		erlang-%{realname}
Version:	2.0.3
Release:	1%{?dist}
Summary:    Syslog backend for Lager
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/riak_core
# wget --content-disposition https://github.com/basho/lager_syslog/tarball/2.0.3
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz

Patch1:     erlang-lager_syslog-2.0.3-relax-deps.patch

BuildRequires:  erlang-lager >= 2.0.3
BuildRequires:	erlang-rebar = 2.6.1
BuildRequires:  erlang-syslog >= 1.0.2

# Error:erlang(dtrace:put_utag/1)
Requires:	erlang-kernel%{?_isa}
Requires:	erlang-stdlib%{?_isa} >= R13B


%description
Distributed systems infrastructure used by Riak.


%prep
%setup -q -n %{upstream}-%{realname}-560a477
%patch1 -p1

%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,priv}
install -p -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin


%check
rebar eunit skip_deps=true -v || :


%files
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam


%changelog
* Thu Jul  9 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.0.3-1
- Initial package
