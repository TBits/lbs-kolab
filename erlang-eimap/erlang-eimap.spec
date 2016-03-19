%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname eimap
%global debug_package %{nil}

Name:		erlang-%{realname}
Version:	0.2
Release:	0.20160111.git%{?dist}
Summary:	Erlang IMAP client
Group:		Development/Libraries
License:	BSD
URL:		http://git.kolab.org/diffusion/EI/%{realname}.git
%if 0%{?el7}%{?fedora}
VCS:		scm:git:https://git.kolab.org/diffusion/EI/%{realname}.git
%endif
Source0:	erlang-eimap-0.2.tar.gz

BuildRequires:	erlang-goldrush >= 0.1.6
BuildRequires:	erlang-lager >= 2.1.0
BuildRequires:	erlang-rebar >= 2.5.1

Requires:	erlang-erts%{?_isa} >= R13B
Requires:	erlang-stdlib%{?_isa} >= R13B

%description
IMAP client library for Erlang

%prep
%setup -q

%build
rebar compile -v

%check
# BEWARE rebar needs bootstrapped getopt in case of an API change
rebar eunit -v

%install
mkdir -p \
    %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/ \
    %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/src/

install -D -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -D -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/.
install -D -m 644 src/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/src/

%files
%doc README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/src/
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/src/*.hrl

%changelog
* Mon Dec 21 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.1.2-1
- First package