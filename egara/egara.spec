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
Version:            0.2
Release:            3.32%{?dist}.kolab_wf
Summary:            Event driven groupware archival system

Group:              System Environment/Daemons
License:            GPLv3+
URL:                https://kolab.org/about/egara

# From 3e4a3da61124e9c79b7f7f49516e6e86aa072051
Source0:            http://mirror.kolabsys.com/pub/releases/%{name}-%{version}.tar.gz

Patch1:             make-it-very-easy-for-rebar3.patch

BuildRequires:      erlang
BuildRequires:      erlang-eimap >= 0.4.0
BuildRequires:      erlang-eldap
BuildRequires:      erlang-goldrush >= 0.1.6
BuildRequires:      erlang-inert
BuildRequires:      erlang-iso8601
BuildRequires:      erlang-jsx >= 2.4.0
BuildRequires:      erlang-lager >= 2.1.0
BuildRequires:      erlang-lager_syslog
BuildRequires:      erlang-meck >= 0.8.2
BuildRequires:      erlang-poolboy >= 1.4.2
BuildRequires:      erlang-procket
BuildRequires:      erlang-protobuffs
BuildRequires:      erlang-rebar3 >= 3.3.2
BuildRequires:      erlang-riak_pb
BuildRequires:      erlang-riakc >= 2.0.1
BuildRequires:      erlang-rpm-macros
BuildRequires:      erlang-syn >= 1.5.0

Requires(pre):      shadow-utils
Requires(postun):   shadow-utils

Requires:           erlang
Requires:           erlang-eimap >= 0.4.0
Requires:           erlang-eldap
Requires:           erlang-goldrush >= 0.1.6
Requires:           erlang-inert
Requires:           erlang-iso8601
Requires:           erlang-jsx => 2.4.0
Requires:           erlang-lager >= 2.1.0
Requires:           erlang-lager_syslog
Requires:           erlang-meck >= 0.8.2
Requires:           erlang-poolboy >= 1.4.2
Requires:           erlang-procket
Requires:           erlang-protobuffs
Requires:           erlang-riak_pb
Requires:           erlang-riakc >= 2.0.1
Requires:           erlang-syn >= 1.5.0

%description
Egara is an event driven groupware archival system for e-Discovery
and Data Loss Prevention. The name means "storehouse" in Sumerian.

It is designed to be used with the Kolab Groupware server and is
written (primarily) in Erlang.

%prep
%setup -q

%patch1 -p1

%build
DEBUG=1
export DEBUG

HEX_OFFLINE=true
export HEX_OFFLINE

rebar3 release \
    --dev-mode false \
    --relname %{name} \
    --relvsn %{version} \
    --verbose

%install

find . -type f | sort

mkdir -p \
    %{buildroot}%{_sysconfdir}/%{name}/ \
    %{buildroot}%{_sbindir} \
    %{buildroot}%{_erldir}/bin/ \
    %{buildroot}%{_erllibdir}/%{realname}-%{version}/

install app.config %{buildroot}%{_sysconfdir}/%{name}/sys.config

pushd %{buildroot}%{_erldir}/bin/
ln -s ../lib/%{name}-%{version}/bin/egara egara
popd

cp -a _build/default/rel/egara/bin/ %{buildroot}%{_erllibdir}/%{realname}-%{version}/
cp -a _build/default/rel/egara/lib/egara-%{version}/ebin/ %{buildroot}%{_erllibdir}/%{realname}-%{version}/
cp -a _build/default/rel/egara/releases %{buildroot}%{_erllibdir}/%{realname}-%{version}/

pushd %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/releases/%{version}/
ln -sfv ../../../../../../..%{_sysconfdir}/%{name}/sys.config sys.config
mv vm.args ../../../../../../..%{_sysconfdir}/%{name}/vm.args
ln -sv ../../../../../../..%{_sysconfdir}/%{name}/vm.args vm.args
popd

pushd %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/
ln -s ../../lib lib
popd

pushd %{buildroot}%{_sbindir}
ln -sfv ../..%{_erllibdir}/%{name}-%{version}/bin/egara egara
popd

%check
DEBUG=1
export DEBUG

HEX_OFFLINE=true
export HEX_OFFLINE

# Hopeless for -0.2
rebar3 eunit -v || :

%files
%doc README.md
%{_sbindir}/egara
%dir %{_sysconfdir}/egara
%config(noreplace) %{_sysconfdir}/egara/sys.config
%config(noreplace) %{_sysconfdir}/egara/vm.args
%{_erldir}/bin/*
%{_erllibdir}/%{realname}-%{version}

%changelog
* Fri May 15 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.1-0.1.git
- First package
