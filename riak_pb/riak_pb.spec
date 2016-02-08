%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%if 0%{?fedora} < 13 && 0%{?rhel} < 6
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

%global realname riak_pb
%global upstream basho
# Techincally, we're noarch; but erlang whose directories we install into is not.
%global debug_package %{nil}
%global git_tag 620bc70
%global patchnumber 0

Name:           riak_pb
Version:        2.1.0.2
Release:        1%{?dist}
Summary:        Riak Protocol Buffers Messages
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://basho.github.com/riak_pb

# From wget --content-disposition https://github.com/basho/riak_pb/tarball/2.1.0.2
Source0:        %{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz

Patch1:         basho-riak_pb-fc18a9b-version.patch
Patch2:         basho-riak_pb-fc18a9b-encoding_test.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Riak Protocol Buffers Messages

%package -n erlang-riak_pb
Summary:        Erlang library for Riak Protocol Buffers Messages
Group:          Development/Libraries

BuildRequires:  erlang-meck >= 0.1
BuildRequires:  erlang-protobuffs >= 0.8
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

%package -n python-riak_pb
Summary:        Python client library for Riak Protocol Buffers Messages
Group:          Development/Libraries

%if 0%{?suse_version}
BuildRequires:	python-devel
%else
BuildRequires:  python2-devel
%endif
BuildRequires:	python-setuptools

Requires:       protobuf-python

%description -n python-riak_pb
Python client for Riak

%prep
%setup -q -n %{upstream}-%{realname}-62d6887
%patch1 -p1
%patch2 -p1

%build
rebar compile -v
%{__python} setup.py build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include
install -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 include/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include
install -m 644 rebar.config %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/rebar.config

%{__python} setup.py install --skip-build --prefix=%{_prefix} --root %{buildroot}

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

%files -n python-riak_pb
%defattr(-,root,root,-)
%doc README.md
%{python_sitelib}/riak_pb
%{python_sitelib}/*.egg-info

%changelog
* Fri Dec  5 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.0.0.16-1
- First package
