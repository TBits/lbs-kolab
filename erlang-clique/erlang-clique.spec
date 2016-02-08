%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname clique
%global upstream basho
%global debug_package %{nil}
%global git_tag ce3bdf7
%global patchnumber 0


Name:		erlang-%{realname}
Version:	0.3.0
Release:	1%{?dist}
Summary:	Distributed systems infrastructure used by Riak
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/clique
# wget --content-disposition https://github.com/basho/clique/tarball/0.3.0
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz

Patch1:     erlang-clique-0.3.0-set-version.patch
# Required for unit-tests only (if you're not interested in a compile-time
# testing then you may remove these lines):
BuildRequires:	erlang-cuttlefish

# Compile-time requirements
BuildRequires:	erlang-rebar

# Error:erlang(dtrace:put_utag/1)
Requires:	erlang-cuttlefish%{?_isa}
Requires:	erlang-erts%{?_isa} >= R13B
Requires:	erlang-kernel%{?_isa}
Requires:	erlang-stdlib%{?_isa} >= R13B


%description
Distributed systems infrastructure used by Riak.


%prep
%setup -q -n %{upstream}-%{realname}-ce3bdf7
%patch1 -p1


%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,include,priv}
install -p -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 644 include/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include


%check
rebar eunit skip_deps=true -v


%files
%doc LICENSE README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/*.hrl


%changelog
* Wed Jul  8 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3.0-1
- First package
