%if 0%{?opensuse_bs}
#!BuildIgnore:  leveldb-devel
#!BuildIgnore:  ghostscript-x11
%endif

%global realname riak_ensemble
%global debug_package %{nil}


Name:		erlang-%{realname}
Version:	2.1.2
Release:	1%{?dist}
Summary:	Distributed systems infrastructure used by Riak
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/riak_ensemble

# wget --content-disposition https://github.com/basho/riak_ensemble/archive/2.1.2.tar.gz
Source0:	%{realname}-%{version}.tar.gz

Patch1:     erlang-riak_ensemble-2.1.2-relax-lager-dep.patch
Patch2:     erlang-riak_ensemble-2.1.2-otp-18.3-compat.patch

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
%setup -q -n %{realname}-%{version}
sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src
%patch1 -p1
%patch2 -p1

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
