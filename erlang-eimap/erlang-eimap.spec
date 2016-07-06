%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname eimap
%global debug_package %{nil}

%define lock_version() %{1}%{?_isa} = %(rpm -q --queryformat "%{VERSION}" %{1})

Name:           erlang-%{realname}
Version:        0.2.5
Release:        0.20160111.git%{?dist}
Summary:        Erlang IMAP client
Group:          Development/Libraries
License:        GPLv3+
URL:            http://git.kolab.org/diffusion/EI/%{realname}.git
%if 0%{?el7}%{?fedora}
VCS:            scm:git:https://git.kolab.org/diffusion/EI/%{realname}.git
%endif
Source0:        erlang-eimap-0.2.5.tar.gz

BuildRequires:	erlang-goldrush >= 0.1.7
BuildRequires:	erlang-lager >= 2.2.0
BuildRequires:	erlang-rebar >= 2.5.1

Requires:       %lock_version erlang-erts
Requires:       %lock_version erlang-stdlib

%description
IMAP client library for Erlang

%prep
%setup -q -n eimap-%{version}

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

%files
%doc README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/src/
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam

%changelog
* Tue Jul  5 2016 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.2.5-1
- Packaging of 0.2.5

* Wed Jun 08 2016 Aaron Seigo <seigo@kolabsystems.com> - 0.2.4-1
- Packaging of 0.2.4

* Tue Jun 07 2016 Aaron Seigo <seigo@kolabsystems.com> - 0.2.2-1
- Packaging of 0.2.2

* Mon Dec 21 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.1.2-1
- First package
