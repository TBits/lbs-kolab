%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
#!BuildIgnore:  leveldb-devel
%endif

%global realname riak_core
%global upstream basho
%global debug_package %{nil}
%global git_tag 429c22d
%global patchnumber 0


Name:		erlang-%{realname}
Version:	2.1.1
Release:	4%{?dist}
Summary:	Distributed systems infrastructure used by Riak
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/riak_core
# wget --content-disposition https://github.com/basho/riak_core/tarball/1.3.2
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz

Patch1:     erlang-riak_core-2.1.1-relax-deps.patch

# Required for unit-tests only (if you're not interested in a compile-time
# testing then you may remove these lines):
BuildRequires:	erlang-basho_stats >= 1.0.3
BuildRequires:  erlang-clique >= 0.2.6
BuildRequires:  erlang-eleveldb >= 2.1.0
BuildRequires:  erlang-exometer_core >= 1.0.0
BuildRequires:	erlang-folsom
BuildRequires:	erlang-lager >= 1.2.2
BuildRequires:	erlang-mochiweb
BuildRequires:  erlang-pbkdf2 >= 2.0.0
BuildRequires:	erlang-poolboy >= 0.8.1
BuildRequires:	erlang-riak_ensemble >= 2.1.0
BuildRequires:	erlang-riak_sysmon >= 1.1.3

# Compile-time requirements
BuildRequires:	erlang-meck >= 0.7.2
BuildRequires:	erlang-rebar
BuildRequires:	erlang-protobuffs >= 0.8.0
BuildRequires:	erlang-webmachine >= 1.9.3

# Error:erlang(dtrace:put_utag/1)
Requires:	erlang-basho_stats%{?_isa}
Requires:	erlang-cluster_info%{?_isa}
Requires:	erlang-crypto%{?_isa}
# Error:erlang(erlang:atom_to_binary/2) in R12B and below
# Error:erlang(erlang:binary_to_atom/2) in R12B and below
# Error:erlang(erlang:max/2) in R12B and below
# Error:erlang(erlang:min/2) in R12B and below
# Error:erlang(lists:keyfind/3) in R12B and below
# Error:erlang(os:timestamp/0) in R12B and below
Requires:	erlang-erts%{?_isa} >= R13B
Requires:	erlang-folsom%{?_isa}
Requires:	erlang-inets%{?_isa}
Requires:	erlang-kernel%{?_isa}
Requires:	erlang-lager%{?_isa}
Requires:	erlang-mochiweb%{?_isa}
Requires:	erlang-poolboy%{?_isa}
Requires:	erlang-protobuffs%{?_isa}
Requires:	erlang-riak_sysmon%{?_isa}
# Error:erlang(dyntrace:p/0) in R14B and below
# Error:erlang(dyntrace:put_tag/1) in R14B and below
Requires:	erlang-runtime_tools%{?_isa} >= R15B
# Error:erlang(ssl:ssl_accept/3) in R12B and below
Requires:	erlang-ssl%{?_isa} >= R13B
# Error:erlang(supervisor:count_children/1) in R12B and below
Requires:	erlang-stdlib%{?_isa} >= R13B
Requires:	erlang-webmachine%{?_isa}


%description
Distributed systems infrastructure used by Riak.


%prep
%setup -q -n %{upstream}-%{realname}-5108231
sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src
%patch1 -p1

%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,include,priv}
install -p -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 644 include/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include
install -p -m 644 priv/* %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/.

%check
rebar eunit skip_deps=true -v || :


%files
%doc LICENSE README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/*.hrl
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/*


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jul 02 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.2-1
- Ver. 1.3.2

* Sun Mar 24 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.1-2
- Fix webmachine dep

* Sun Mar 24 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.1-1
- Ver. 1.3.1

* Mon Mar 11 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.0-1
- Ver. 1.3.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-4.p1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Oct 20 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.1-3.p1
- Ver. 1.2.1p1

* Fri Oct 19 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.1-2
- Rebuild with new lager

* Wed Oct 10 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.1-1
- Ver. 1.2.1

* Wed Sep 05 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.0-1
- Ver. 1.2.0

* Thu Jul 19 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.2-3
- Re-export one handy function

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 18 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.2-1
- Ver. 1.1.2

* Fri Feb 25 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.14.1-1
- Ver. 0.14.1

* Sat Jan 22 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.14.0-1
- Ver. 0.14.0
- Dropped upstreamed patch

* Fri Nov 12 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.13.0-1
- Initial build

