%if 0%{?opensuse_bs}
#!BuildIgnore:  leveldb-devel
#!BuildIgnore:  ghostscript-x11
%endif

%global realname riak_ensemble
%global upstream basho
%global debug_package %{nil}
%global git_tag a69f484
%global patchnumber 0


Name:		erlang-%{realname}
Version:	2.1.0
Release:	1%{?dist}
Summary:	Distributed systems infrastructure used by Riak
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/riak_core
# wget --content-disposition https://github.com/basho/riak_ensemble/tarball/2.1.0
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz

Patch1:     erlang-riak_ensemble-relax-lager-dep.patch

# Required for unit-tests only (if you're not interested in a compile-time
# testing then you may remove these lines):
BuildRequires:  erlang-eleveldb >= 2.1.0
BuildRequires:	erlang-lager >= 1.2.2

# Compile-time requirements
BuildRequires:	erlang-meck >= 0.7.2
BuildRequires:	erlang-rebar

# Error:erlang(dtrace:put_utag/1)
Requires:	erlang-eleveldb%{?_isa}
Requires:	erlang-lager%{?_isa}


%description
Distributed systems infrastructure used by Riak.


%prep
%setup -q -n %{upstream}-%{realname}-b346be0
sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src
%patch1 -p1

%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,include,priv}
install -p -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 644 include/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include


%check
rebar eunit skip_deps=true -v || :


%files
%doc README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/*.hrl


%changelog
* Wed Jul  8 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.1.0-1
- First package
