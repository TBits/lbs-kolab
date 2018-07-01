%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname eimap
%global debug_package %{nil}

%define lock_version() %{1}%{?_isa} = %(rpm -q --queryformat "%%{VERSION}" %{1})

Name:           erlang-%{realname}
Version:        0.4.0
Release:        1%{?dist}
Summary:        Erlang IMAP client
Group:          Development/Libraries
License:        GPLv3+
URL:            http://git.kolab.org/diffusion/EI/%{realname}.git
%if 0%{?el7}%{?fedora}
VCS:            scm:git:https://git.kolab.org/diffusion/EI/%{realname}.git
%endif
Source0:        erlang-eimap-%{version}.tar.gz

Patch1:         untagged-commands.patch
Patch2:         make-things-easy-for-rebar3.patch

BuildRequires:	erlang-goldrush
BuildRequires:	erlang-lager
BuildRequires:	erlang-rebar3 >= 3.3.2

Requires:       %lock_version erlang-erts
Requires:       %lock_version erlang-stdlib

%description
IMAP client library for Erlang

%prep
%setup -q -n eimap-%{version}

%patch1 -p1
%patch2 -p1

%build
DEBUG=1
export DEBUG

HEX_OFFLINE=true
export HEX_OFFLINE

rebar3 release \
    --dev-mode false \
    --relname %{realname} \
    --relvsn %{version} \
    --verbose

%check
# BEWARE rebar needs bootstrapped getopt in case of an API change
rebar3 eunit -v

%install
find -type f | sort

mkdir -p \
    %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/ \
    %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/src/

pushd _build/default/lib/eimap/
install -D -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -D -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/.
popd

%files
%doc README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/src/
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam

%changelog
* Sun Apr 08 2018 Christoph Erhardt <kolab@sicherha.de> - 0.4.0-1
- Upstream release 0.4.0

* Tue Nov  7 2017 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.2.5-5
- Patch untagged commands

* Tue Jul  5 2016 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.2.5-1
- Packaging of 0.2.5

* Wed Jun 08 2016 Aaron Seigo <seigo@kolabsystems.com> - 0.2.4-1
- Packaging of 0.2.4

* Tue Jun 07 2016 Aaron Seigo <seigo@kolabsystems.com> - 0.2.2-1
- Packaging of 0.2.2

* Mon Dec 21 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.1.2-1
- First package
