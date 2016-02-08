
%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname procket
%global upstream msantos
# Technically, we're noarch; but erlang whose directories we install into is not.
%global debug_package %{nil}
%global git_tag 36a8bd3
%global patchnumber 0


Name:           erlang-%{realname}
Version:        0.6.1
Release:        1%{?dist}
Summary:        Socket creation and manipulation for Erlang
Group:          Development/Libraries
License:        GPLv3+
URL:            http://msantos.github.com/procket/
# wget --content-disposition https://github.com/msantos/procket/tarball/0.6.1
Source0:        %{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz

BuildRequires:  erlang-rebar

Requires:       erlang-compiler%{?_isa}
Requires:       erlang-erts%{?_isa}
Requires:       erlang-kernel%{?_isa}
Requires:       erlang-stdlib%{?_isa}
# Error:erlang(cover:compile_beam/2)
# Error:erlang(cover:get_term/1)
# Error:erlang(cover:write/2)
Requires:       erlang-tools%{?_isa}


%description
procket is an Erlang library for socket creation and manipulation.

procket can use a setuid helper so actions like binding low ports and
requesting some sockets types can be done while Erlang is running as an
unprivileged user.

%prep
%setup -q -n %{upstream}-%{realname}-%{git_tag}


%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include
install -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 include/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include


%check
rebar eunit -v


%files
%doc README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/*.hrl

%changelog
* Sun May 17 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.6.1-1
- First package
