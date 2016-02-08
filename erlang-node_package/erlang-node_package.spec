%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname node_package
%global debug_package %{nil}


Name:		erlang-%{realname}
Version:	2.0.3
Release:	1%{?dist}
Summary:	Erlang RPM/Debian/Solaris templates and scripts
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/node_package
%if 0%{?el7}%{?fedora}
VCS:		scm:git:https://github.com/basho/node_package.git
%endif
Source0:	https://github.com/basho/node_package/archive/%{version}/%{realname}-%{version}.tar.gz
BuildRequires:	erlang-rebar
Requires:	erlang-erts%{?_isa}
Requires:	erlang-kernel%{?_isa}
Requires:	erlang-stdlib%{?_isa}


%description
RPM/Debian/Solaris templates and scripts.


%prep
%setup -q -n %{realname}-%{version}
sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src


%build
ERLANG_BIN=%{_bindir} ; export ERLANG_BIN
rebar compile -v
rebar doc -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,priv}
install -p -m 0644 -D ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
cp -a priv/* %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/.


%files
%doc LICENSE README.org
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/priv


%changelog
* Wed Jul  8 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.0.3-1
- Initial package
