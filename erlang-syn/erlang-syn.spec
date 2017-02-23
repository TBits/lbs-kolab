%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname syn
%global upstream ostinelli
# Techincally, we're noarch; but erlang whose directories we install into is not.
%global debug_package %{nil}
%global git_tag d43b232
%global patchnumber 0


Name:           erlang-%{realname}
Version:        1.6.0
Release:        1%{?dist}
Summary:        Process Registry and Process Group manager for Erlang
Group:          Development/Libraries
License:        ASL 2.0
URL:            http://eproxus.github.com/syn/
# wget --content-disposition https://github.com/ostinelli/syn/tarball/1.6.0
Source0:        %{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz

BuildRequires:  erlang-rebar

%description
A global Process Registry allows registering a process on all the nodes of a
cluster with a single Key. Consider this the process equivalent of a DNS
server: in the same way you can retrieve an IP address from a domain name, you
can retrieve a process from its Key.

%prep
%setup -q -n %{upstream}-%{realname}-%{git_tag}

%build
rebar compile -v

%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include

find . -type f | sort

install -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 include/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include
install -m 644 rebar.config %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/

%check
rebar -C test.config skip_deps=true eunit -v || :

%files
%doc LICENSE.md README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/*.hrl
%{_libdir}/erlang/lib/%{realname}-%{version}/rebar.config

%changelog
* Mon Feb  6 2017 Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com> - 1.6.0-1
- First package
