%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname goldrush
%global upstream DeadZen
%global debug_package %{nil}

Name:		erlang-%{realname}
Version:	0.1.6
Release:	1%{?dist}
Summary:	Fast event stream processing
Group:		Development/Languages
License:	ASL 2.0
URL:		http://github.com/%{upstream}/%{realname}
%if 0%{?el7}%{?fedora}
VCS:		scm:git:https://github.com/%{upstream}/%{realname}.git
%endif
Source0:	https://github.com/%{upstream}/%{realname}/archive/%{version}/%{realname}-%{version}.tar.gz
BuildRequires:	erlang-rebar
Requires:	erlang-compiler%{?_isa}
# Error:erlang(erlang:max/2) in R12B and below
# Error:erlang(erlang:min/2) in R12B and below
# Error:erlang(lists:keyfind/3) in R12B and below
# Error:erlang(os:timestamp/0) in R12B and below
Requires:	erlang-erts%{?_isa} >= R13B
# Error:erlang(file:datasync/1) in R13B and below
Requires:	erlang-kernel%{?_isa} >= R14B
# Error:erlang(unicode:characters_to_list/1) in R12B and below
Requires:	erlang-stdlib%{?_isa} >= R13B
Requires:	erlang-syntax_tools%{?_isa}

%description
Goldrush is a small Erlang app that provides fast event stream
processing

%prep
%setup -q -n %{realname}-%{version}

%build
rebar compile -v

%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 0644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -p -m 0644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 0644 rebar.config %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/rebar.config

%check
rebar eunit -v

%files
%doc LICENSE README.org
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/rebar.config

%changelog
* Fri May 15 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.1.6-1
- Check in 0.1.6

