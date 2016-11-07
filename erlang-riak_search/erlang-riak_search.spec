%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname riak_search
#
# This package contains only arch-independent data but install it into
# arch-dependent directory thus making this package arch-dependent. In order to
# suppress empty *-debuginfo generation we have to explicitly order
# debuginfo-generator to skip trying to build *-debuiginfo for that package.
#
%global debug_package %{nil}
%global patchnumber 0


Name:		erlang-%{realname}
Version:	2.1.1
Release:	1%{?dist}
Summary:	Full-text search engine based on Riak
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/riak_search
%if 0%{?rhel} > 6 || 0%{?fedora}
VCS:		https://github.com/basho/riak_search.git
%endif
Source0:	https://github.com/basho/riak_search/archive/%{version}/%{realname}-%{version}.tar.gz
# Fedora/EPEL-specific
Patch1:		erlang-riak_search-0001-Relax-dependencies.patch
# Backported from upstream
Patch2:		erlang-riak_search-0002-use-tuple-modules-instead-of-parameterized-modules.patch
# Fedora/EPEL-specific
Patch3:		erlang-riak_search-0003-Fix-version.patch
# Fedora/EPEL-specific
Patch4:		erlang-riak_search-0004-Move-tests-to-the-canonical-directory.patch
BuildRequires:	erlang-lager
BuildRequires:	erlang-merge_index >= 1.3.0
BuildRequires:	erlang-parsetools
BuildRequires:	erlang-rebar
BuildRequires:	erlang-riak_api >= 1.3.2
BuildRequires:	erlang-riak_core >= 1.3.2
BuildRequires:	erlang-riak_kv >= 1.3.2
BuildRequires:	erlang-riak_pb >= 1.3.2
BuildRequires:	erlang-riak_pipe >= 1.3.2
BuildRequires:	erlang-webmachine
# Error:erlang(basho_bench_config:get/1)
# Error:erlang(basho_bench_config:get/2)
Requires:	erlang-cluster_info%{?_isa}
Requires:	erlang-crypto%{?_isa}
Requires:	erlang-erts%{?_isa}
Requires:	erlang-eunit%{?_isa}
Requires:	erlang-folsom%{?_isa}
Requires:	erlang-inets%{?_isa}
Requires:	erlang-kernel%{?_isa}
Requires:	erlang-lager%{?_isa}
Requires:	erlang-merge_index%{?_isa}
Requires:	erlang-mochiweb%{?_isa}
Requires:	erlang-riak_api%{?_isa}
Requires:	erlang-riak_core%{?_isa}
Requires:	erlang-riak_kv%{?_isa}
Requires:	erlang-riak_pb%{?_isa}
Requires:	erlang-riak_pipe%{?_isa}
Requires:	erlang-stdlib%{?_isa}
Requires:	erlang-webmachine%{?_isa}
Requires:	erlang-xmerl%{?_isa}


%description
The riak_search OTP application provides Riak with the capability to act as a
text search engine similar to Apache’s Lucene. Previously Riak Search was a
release in it’s own right. Since then Basho has decided it would be easier for
our users if Search was simply a set of functionality that can be enabled via a
config option. For that reason, if you want to use Search you’ll have to build
a Riak release and enable it.


%prep
%setup -q -n %{realname}-%{version}
sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src
#%patch1 -p1 -b .fix_deps
# reverse
#%patch2 -p1 -b .r16b
#%patch3 -p1 -b .ver
%patch4 -p1 -b .tests
# remove bundled rebar copies - just to be absolutely sure
rm -f ./rebar ./apps/lucene_parser/rebar


%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/lucene_parser-1/{ebin,include}
install -p -m 0644 apps/lucene_parser/ebin/lucene_parser.app %{buildroot}%{_libdir}/erlang/lib/lucene_parser-1/ebin/lucene_parser.app
install -p -m 0644 apps/lucene_parser/ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/lucene_parser-1/ebin
install -p -m 0644 apps/lucene_parser/include/*.hrl %{buildroot}%{_libdir}/erlang/lib/lucene_parser-1/include/

mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,include,priv}
install -p -m 0644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -p -m 0644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 0644 include/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include/
install -p -m 0644 priv/default.def %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/


%check
rebar eunit skip_deps=true -v || :


%files
%doc doc/ releasenotes/ LICENSE README.org THANKS
%dir %{_libdir}/erlang/lib/lucene_parser-1
%dir %{_libdir}/erlang/lib/lucene_parser-1/ebin
%dir %{_libdir}/erlang/lib/lucene_parser-1/include
%{_libdir}/erlang/lib/lucene_parser-1/ebin/lucene_parser.app
%{_libdir}/erlang/lib/lucene_parser-1/ebin/*.beam
%{_libdir}/erlang/lib/lucene_parser-1/include/*.hrl
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/*.hrl
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/default.def


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

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2.p2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Nov 18 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.1-1.p2
- Ver. 1.2.1p2

* Sun Jul 29 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.4-1
- Ver. 1.1.4 (fully API compatible with 1.1.2)
- Removed sed invocation
- Consistently use macros

* Thu May 17 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.2-1
- Initial package

