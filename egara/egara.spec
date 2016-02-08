%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global debug_package %{nil}

%global realname egara

%global egara_user egara
%global egara_group egara
%global mail_group mail
%global mail_group_id 76

Name:               egara
Version: 0.2
Release: 0.20150708.git%{?dist}
Summary:            Event driven groupware archival system

Group:              System Environment/Daemons
License:            GPLv3+
URL:                https://kolab.org/about/egara

# From 3e4a3da61124e9c79b7f7f49516e6e86aa072051
Source0:            http://mirror.kolabsys.com/pub/releases/%{name}-%{version}.tar.gz

Patch1:             egara-0.1-tests.patch
Patch2:             egara-0.1-release.patch

BuildRequires:      erlang
BuildRequires:      erlang-eldap
BuildRequires:      erlang-goldrush >= 0.1.6
BuildRequires:      erlang-inert
BuildRequires:      erlang-iso8601
BuildRequires:      erlang-jsx >= 2.4.0
BuildRequires:      erlang-lager >= 2.1.0
BuildRequires:      erlang-meck >= 0.8.2
BuildRequires:      erlang-poolboy >= 1.4.2
BuildRequires:      erlang-procket
BuildRequires:      erlang-protobuffs
BuildRequires:      erlang-rebar
BuildRequires:      erlang-riak_pb
BuildRequires:      erlang-riakc >= 2.0.1

Requires(pre):      shadow-utils
Requires(postun):   shadow-utils

Requires:           erlang
Requires:           erlang-eldap
Requires:           erlang-goldrush >= 0.1.6
Requires:           erlang-inert
Requires:           erlang-iso8601
Requires:           erlang-jsx => 2.4.0
Requires:           erlang-lager >= 2.1.0
Requires:           erlang-meck >= 0.8.2
Requires:           erlang-poolboy >= 1.4.2
Requires:           erlang-procket
Requires:           erlang-protobuffs
Requires:           erlang-riak_pb
Requires:           erlang-riakc >= 2.0.1

%description
Egara is an event driven groupware archival system for e-Discovery
and Data Loss Prevention. The name means "storehouse" in Sumerian.

It is designed to be used with the Kolab Groupware server and is
written (primarily) in Erlang.

%prep
%setup -q
%patch1 -p1
%patch2 -p1

%build
pushd rel
rebar create-node nodeid=egara
popd
ENABLE_STATIC=no rebar compile -v
rebar generate -v

%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 apps/egara/ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 apps/egara/ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin

%check
rebar skip_deps=true eunit -v

%pre
if [ $1 == 1 ]; then
    /usr/sbin/groupadd -g %{mail_group_id} --system %{mail_group} 2> /dev/null || :
    /usr/sbin/groupadd --system %{egara_group} 2> /dev/null || :
    /usr/sbin/useradd -c "Egara Service" -d %{_var}/lib/egara -g %{egara_group} \
        -G %{mail_group} -s /sbin/nologin --system %{egara_user} 2> /dev/null || :
fi

%postun
if [ $1 == 0 ]; then
    /usr/sbin/userdel %{egara_user} 2>/dev/null || :
    /usr/sbin/groupdel %{egara_group} 2>/dev/null || :
fi

%files
%doc README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam

%changelog
* Fri May 15 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.1-0.1.git
- First package
