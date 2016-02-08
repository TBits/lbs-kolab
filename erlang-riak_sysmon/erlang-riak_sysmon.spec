%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname riak_sysmon
%global upstream basho
%global debug_package %{nil}
%global git_tag abe744c
%global patchnumber 0


Name:		erlang-%{realname}
Version:	2.1.1
Release:	1%{?dist}
Summary:	Rate-limiting system_monitor event handler for Riak
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/riak_sysmon
# From https://github.com/basho/riak_sysmon/archive/2.1.1.tar.gz
Source0:	%{realname}-%{version}.tar.gz
BuildRequires:	erlang-cuttlefish
BuildRequires:	erlang-rebar
Requires:	erlang-erts%{?_isa}
Requires:	erlang-kernel%{?_isa}
Requires:	erlang-stdlib%{?_isa}


%description
Simple OTP app for managing Erlang VM system_monitor event messages.


%prep
%setup -q -n %{realname}-%{version}

%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,priv}
install -p -m 0644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -p -m 0644 ebin/%{realname}_*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 0644 priv/*.schema %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv

%check
epmd -daemon
rebar eunit skip_deps=true -v
epmd -kill


%files
%doc LICENSE README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/*.schema


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.1.3-2
- Fix file layout

* Mon Mar 11 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.1.3-1
- Ver. 1.1.3

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.2-3
- Stop epmd gracefully after running tests

* Tue May 22 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.2-2
- Fixed tests

* Tue May 15 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.2-1
- Ver. 1.1.2

* Fri Sep 16 2011 Peter Lemenkov <lemenkov@gmail.com> - 1.0.0-1
- Ver. 1.0.0
