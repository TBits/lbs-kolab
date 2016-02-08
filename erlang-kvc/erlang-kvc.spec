%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname kvc
%global debug_package %{nil}


Name:		erlang-%{realname}
Version:	1.5.0
Release:	1%{?dist}
Summary:	Key Value Coding for Erlang data structures
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/etrepum/kvc
%if 0%{?el7}%{?fedora}
VCS:		scm:git:https://github.com/etrepum/kvc.git
%endif
Source0:	https://github.com/etrepum/kvc/archive/%{version}/%{realname}-%{version}.tar.gz

BuildRequires:	erlang-rebar

Requires:	erlang-kernel%{?_isa}
Requires:	erlang-stdlib%{?_isa}

%description
kvc supports Key Value Coding-like queries on
common Erlang data structures. A common use case
for kvc is to quickly access one or more deep
values in decoded JSON, or some other nested data
structure. It can also help with some aggregate
operations. It solves similar problems that you
might want to use a tool like XPath or jQuery for,
but it is far simpler and strictly less powerful.

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
* Thu Jul  9 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.5.0-1
- Initial package
