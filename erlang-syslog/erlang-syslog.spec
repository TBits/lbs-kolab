%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname syslog
%global debug_package %{nil}


Name:		erlang-%{realname}
Version:	1.0.3
Release:	1%{?dist}
Summary:	Syslog driver for Erlang
Group:		Development/Languages
License:	MIT
URL:		https://github.com/Vagabond/erlang-syslog
%if 0%{?el7}%{?fedora}
VCS:		scm:git:https://github.com/Vagabond/erlang-syslog.git
%endif
Source0:	https://github.com/Vagabond/erlang-syslog/archive/%{version}/erlang-%{realname}-%{version}.tar.gz

BuildRequires:	erlang-rebar

%description
This is an erlang port driver for interacting with syslog(3).


%prep
%setup -q


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
