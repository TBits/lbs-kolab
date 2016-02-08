%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname canola
%global debug_package %{nil}


Name:		erlang-%{realname}
Version:	2.0.0
Release:	1%{?dist}
Summary:	Simple PAM port driver for erlang
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/canola
%if 0%{?el7}%{?fedora}
VCS:		scm:git:https://github.com/basho/canola.git
%endif
Source0:	https://github.com/basho/canola/archive/%{version}/%{realname}-%{version}.tar.gz
BuildRequires:	erlang-rebar
BuildRequires:  pam-devel

Requires:	erlang-kernel%{?_isa}
Requires:	erlang-stdlib%{?_isa}


%description
Simple PAM port driver for erlang

%prep
%setup -q -n %{realname}-%{version}
sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src


%build
rebar compile -v
rebar doc -v


%install
install -p -m 0644 -D ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -p -m 0644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin


%files
%doc README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam


%changelog
* Wed Jul  8 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.5-1
- Initial package
