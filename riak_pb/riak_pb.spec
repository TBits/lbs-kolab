%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname riak_pb
%global debug_package %{nil}

Name:           riak_pb
Version:        2.1.4.1
Release:        1%{?dist}
Summary:        Riak Protocol Buffers Messages
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/basho/riak_pb

# wget --content-disposition https://github.com/basho/riak_pb/archive/2.1.4.1.tar.gz
Source0:        %{realname}-%{version}.tar.gz

Patch2:         basho-riak_pb-fc18a9b-encoding_test.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Riak Protocol Buffers Messages

%package -n erlang-riak_pb
Summary:        Erlang library for Riak Protocol Buffers Messages
Group:          Development/Libraries

BuildRequires:  erlang-hamcrest >= 0.3
BuildRequires:  erlang-meck >= 0.1
BuildRequires:  erlang-protobuffs >= 0.8.4
BuildRequires:  erlang-rebar

Requires:       erlang-compiler%{?_isa}
Requires:       erlang-erts%{?_isa}
Requires:       erlang-kernel%{?_isa}
Requires:       erlang-stdlib%{?_isa}
# Error:erlang(cover:compile_beam/2)
# Error:erlang(cover:get_term/1)
# Error:erlang(cover:write/2)
Requires:       erlang-tools%{?_isa}
Requires:       erlang-protobuffs >= 0.8

%description -n erlang-riak_pb

%prep
%setup -q -n %{realname}-%{version}
sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src
%patch2 -p1

%build
rebar compile -v

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include
install -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 include/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include
install -m 644 rebar.config %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/rebar.config

%check
rebar skip_deps=true eunit -v

%clean
rm -rf %{buildroot}

%files -n erlang-riak_pb
%defattr(-,root,root,-)
%doc README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/*.hrl
%{_libdir}/erlang/lib/%{realname}-%{version}/rebar.config

%changelog
* Fri Dec  5 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.0.0.16-1
- First package
