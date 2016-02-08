%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname riak_kv
#
# This package contains only arch-independent data but install it into
# arch-dependent directory thus making this package arch-dependent. In order to
# suppress empty *-debuginfo generation we have to explicitly order
# debuginfo-generator to skip trying to build *-debuiginfo for that package.
#
%global debug_package %{nil}
%global patchnumber 0


Name:		erlang-%{realname}
Version:	2.1.0
Release:	1%{?dist}
Summary:	Riak Key/Value Store
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/riak_kv
VCS:		https://github.com/basho/riak_kv.git
Source0:	https://github.com/basho/riak_kv/archive/%{version}/%{realname}-%{version}.tar.gz
# Fedora/EPEL specific patch
Patch1:		erlang-riak_kv-0001-Use-system-wide-mochijson2.patch
# Will be proposed for inclusion to upstream
Patch2:		erlang-riak_kv-0002-Guard-eunit-include-to-prevent-automatic-dependency-.patch
# https://github.com/basho/riak_kv/pull/469
Patch3:		erlang-riak_kv-0003-use-tuple-modules-instead-of-parameterized-modules.patch
# Fedora/EPEL specific patch
Patch4:		erlang-riak_kv-0004-Don-t-fail-on-warnings.patch
# Fedora/EPEL specific patch
Patch5:		erlang-riak_kv-0005-Relax-dependency-checks.patch
# Backported from upstream
Patch6:		erlang-riak_kv-0006-Move-setting-bucket-properties-to-riak_api-see-basho.patch
# Fedora/EPEL specific patch
Patch7:		erlang-riak_kv-0007-Fix-module-loading-order-for-tests.patch
# Backported from upstream
Patch8:		erlang-riak_kv-0008-migrate-mapred_test-to-riak_test.patch
# Fedora/EPEL specific patch
Patch9:		erlang-riak_kv-0009-Allow-building-against-bitcask-1.6.3.patch
# Fedora/EPEL specific patch
Patch10:	erlang-riak_kv-0010-Fix-for-Erlang-R16B01.patch

Patch11:    erlang-riak_kv-2.1.0-default-storage-backend-memory.patch

BuildRequires:	erlang-bitcask >= 1.6.2
BuildRequires:	erlang-ebloom >= 1.1.2
BuildRequires:	erlang-eleveldb >= 1.3.2
BuildRequires:	erlang-eper >= 0.78
BuildRequires:	erlang-eunit_formatters >= 0.1.2
BuildRequires:  erlang-exometer_core
BuildRequires:	erlang-js >= 1.3.0
BuildRequires:	erlang-merge_index >= 1.3.0
BuildRequires:	erlang-os_mon
BuildRequires:	erlang-rebar
BuildRequires:	erlang-riak_api >= 1.3.2
BuildRequires:	erlang-riak_dt
BuildRequires:  erlang-riak_ensemble
BuildRequires:	erlang-riak_core >= 1.3.2
BuildRequires:	erlang-riak_pipe >= 1.3.2
BuildRequires:	erlang-sext >= 1.1
BuildRequires:	erlang-sidejob >= 0.2.0
# Error:erlang(dtrace:init/0)
Requires: erlang-bitcask%{?_isa} >= 1.6.2
Requires: erlang-cluster_info%{?_isa}
Requires: erlang-crypto%{?_isa}
Requires: erlang-eleveldb%{?_isa} >= 1.3.2
Requires: erlang-erts%{?_isa}
Requires: erlang-eunit%{?_isa}
Requires: erlang-eunit_formatters%{?_isa}
Requires: erlang-exometer_core%{?_isa}
Requires: erlang-folsom%{?_isa}
Requires: erlang-inets%{?_isa}
Requires: erlang-js%{?_isa} >= 1.2.2
Requires: erlang-kernel%{?_isa}
Requires: erlang-lager%{?_isa}
Requires: erlang-mochiweb%{?_isa}
Requires: erlang-os_mon%{?_isa}
Requires: erlang-riak_api%{?_isa} >= 1.3.2
Requires: erlang-riak_core%{?_isa} >= 1.3.2
Requires: erlang-riak_dt%{?_isa}
Requires: erlang-riak_ensemble%{?_isa}
Requires: erlang-riak_pb%{?_isa}
Requires: erlang-riak_pipe%{?_isa} >= 1.3.2
Requires: erlang-runtime_tools%{?_isa}
Requires: erlang-sext%{?_isa} >= 1.1
Requires: erlang-sidejob%{?_isa}
Requires: erlang-stdlib%{?_isa}
Requires: erlang-webmachine%{?_isa}


%description
Riak Key/Value Store.


%prep
%setup -q -n %{realname}-%{version}
sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src
%patch1 -p1 -b .systemwide_mochijson2
#%patch2 -p1 -b .noeunit
# reverse
#%patch3 -p1 -b .r16
#%patch4 -p1 -b .dont_fail_on_warn
#%patch5 -p1 -b .relax_deps
# reverse
#%patch6 -p1 -b .fix_pb
#%patch7 -p1 -b .fix_order
# reverse
#%patch8 -p1 -b .remove_problematic_fragile_test_suite
#%patch9 -p1 -b .relax_bitcask_ver
#%patch10 -p1 -b .r16b01
# remove bundled rebar copy - just to be absolutely sure
rm -f ./rebar

%patch11 -p1 -b .storage-backend-memory

%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,include,priv}
install -p -m 0644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -p -m 0644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 0644 include/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include
install -p -m 0644 src/riak_kv_wm_raw.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include
install -p -m 0755 priv/mapred_builtins.js %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/
install -p -m 0644 priv/*.schema %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/


%check
# Several tests requires epmd to run
epmd -daemon
rebar eunit skip_deps=true -v || true
epmd -kill



%files
%doc docs/* README.org
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv/
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/*.hrl
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/mapred_builtins.js
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/*.schema


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Aug 06 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.2-1
- Ver. 1.3.2

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 24 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.1-1
- Ver. 1.3.1

* Mon Mar 11 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.0-1
- Ver. 1.3.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3.p3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Nov 18 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.1-2.p3
- Ver. 1.2.1p3

* Sat Oct 27 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.1-1.p2
- Ver. 1.2.1p2

* Sun Aug 05 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.4-1
- Ver. 1.1.4 (security bugfix)

* Tue Jun 19 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.2-1
- Ver. 1.1.2

* Sat Feb 26 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.14.1-1
- Ver. 0.14.1

* Sun Jan 23 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.14.0-1
- Ver. 0.14.0

* Fri Nov 12 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.13.0-1
- Initial build

