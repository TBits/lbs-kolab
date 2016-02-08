%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname exometer_core
%global upstream Feuerlabs
%global debug_package %{nil}
%global git_tag d7c4ddd
%global patchnumber 0


Name:		erlang-%{realname}
Version:	1.4
Release:	1%{?dist}
Summary:	Erlang instrumentation package, core services
Group:		Development/Languages
License:	MPL 2.0
URL:		https://github.com/Feuerlabs/exometer_core
# wget --content-disposition https://github.com/Feuerlabs/exometer_core/tarball/1.4
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz

Patch1:     erlang-exometer_core-1.4-set-version.patch

# Required for unit-tests only (if you're not interested in a compile-time
# testing then you may remove these lines):
BuildRequires:	erlang-lager >= 2.0.3
BuildRequires:	erlang-parse_trans >= 2.9.2
BuildRequires:	erlang-folsom >= 0.8.2
BuildRequires:  erlang-setup >= 1.5

# Compile-time requirements
BuildRequires:	erlang-meck >= 0.8.2
BuildRequires:	erlang-rebar

Requires:	erlang-kernel%{?_isa}
Requires:	erlang-lager%{?_isa}
Requires:	erlang-setup%{?_isa}
Requires:	erlang-stdlib%{?_isa} >= R13B


%description
The Exometer Core package allows for easy and efficient
instrumentation of Erlang code, allowing crucial data
on system performance to be exported to a wide variety
of monitoring systems.

Exometer Core comes with a set of pre-defined monitor
components, and can be expanded with custom components
to handle new types of Metrics, as well as integration
with additional external systems such as databases,
load balancers, etc.


%prep
%setup -q -n %{upstream}-%{realname}-21b4194
%patch1 -p1

%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,include,priv}
install -p -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 644 include/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include


%check
rm -rf test/exometer_report_SUITE.erl
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
* Wed Jul  8 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.4-1
- Initial package
