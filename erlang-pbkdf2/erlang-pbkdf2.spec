%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname pbkdf2
%global upstream basho
%global debug_package %{nil}
%global git_tag 7076584
%global patchnumber 0


Name:		erlang-%{realname}
Version:	2.0.0
Release:	1%{?dist}
Summary:	Distributed systems infrastructure used by Riak
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/erlang-pbkdf2
# wget --content-disposition https://github.com/basho/erlang-pbkdf2/tarball/2.0.0
Source0:	%{upstream}-erlang-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz

Patch1:     erlang-pbkdf2-2.0.0-set-version.patch
Patch2:     erlang-pbkdf2-2.0.0-test-timeout.patch

# Compile-time requirements
BuildRequires:	erlang-rebar

Requires:	erlang-stdlib%{?_isa} >= R13B


%description
Distributed systems infrastructure used by Riak.


%prep
%setup -q -n %{upstream}-erlang-%{realname}-3729834
%patch1 -p1
%patch2 -p1

%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,priv}
install -p -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin


%check
rebar eunit skip_deps=true -v


%files
%doc LICENSE README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam


%changelog
* Wed Jul  8 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.0.0-1
- Initial package
