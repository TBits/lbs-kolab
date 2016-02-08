%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname parse_trans
%global upstream uwiger
%global debug_package %{nil}
%global git_tag a210ada
%global patchnumber 0


Name:		erlang-%{realname}
Version:	2.9.2
Release:	1%{?dist}
Summary:	Generic parse transform library for Erlang
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/uwiger/parse_trans
# wget --content-disposition https://github.com/uwiger/parse_trans/tarball/2.9.2
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz

Patch1:     erlang-parse_trans-2.9.2-set-version.patch

# Required for unit-tests only (if you're not interested in a compile-time
# testing then you may remove these lines):
BuildRequires:	erlang-edown >= 0.7

# Compile-time requirements
BuildRequires:	erlang-rebar

Requires:	erlang-edown%{?_isa}
Requires:	erlang-kernel%{?_isa}
Requires:	erlang-syntax_tools%{?_isa}
Requires:	erlang-stdlib%{?_isa} >= R13B


%description
Generic parse transform library for Erlang


%prep
%setup -q -n %{upstream}-%{realname}-8a86b84
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
%doc README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/*.hrl


%changelog
* Wed Jul  8 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.9.2-1
- Initial package
