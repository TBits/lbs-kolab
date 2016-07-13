%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname protobuffs
%global debug_package %{nil}

Name:		erlang-%{realname}
Version:	0.8.4
Release:	1%{?dist}
Summary:	A set of Protocol Buffers tools and modules for Erlang applications
Group:		Development/Libraries
License:	MIT
URL:		http://github.com/basho/erlang_protobuffs
# wget --content-disposition https://github.com/basho/erlang_protobuffs/archive/0.8.4.tar.gz
Source0:	erlang_%{realname}-%{version}.tar.gz
BuildRequires:	erlang-meck
BuildRequires:	erlang-rebar
# This is actually a rebar-related issue, see rhbz #960079
BuildRequires:	erlang-common_test
BuildRequires:	erlang-parsetools
Requires:	erlang-compiler%{?_isa}
# Error:erlang(lists:keyfind/3) in R12B and below
Requires:	erlang-erts%{?_isa} >= R13B
Requires:	erlang-kernel%{?_isa}
# Error:erlang(erl_scan:token_info/2) in R12B and below
# Error:erlang(io_lib:write_unicode_string/1) in R12B and below
# Error:erlang(unicode:characters_to_binary/1) in R12B and below
Requires:	erlang-stdlib%{?_isa} >= R13B
Requires:	erlang-syntax_tools%{?_isa}


%description
A set of Protocol Buffers tools and modules for Erlang applications.


%prep
%setup -q -n erlang_%{realname}-%{version}
sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src


%build
rebar compile -v


%install
find . -type f | sort
install -d %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/.eunit/
install -d %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -m 644 ebin/pokemon_pb.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -m 644 ebin/%{realname}.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -m 644 ebin/%{realname}_cli.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -m 644 ebin/%{realname}_compile.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -m 644 ebin/%{realname}_file.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -m 644 ebin/%{realname}_parser.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -m 644 ebin/%{realname}_scanner.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -m 644 rebar.config %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/

%check
# Escape tests for coverage enabled issues, but disable coverage anyway
sed -i -e '/cover_enabled/d' rebar.config
rebar eunit skip_deps=true -v || :
rebar ct skip_deps=true -v || :


%files
%doc AUTHORS README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/pokemon_pb.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_cli.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_compile.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_file.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_parser.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_scanner.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/rebar.config


%changelog
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Sep 01 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.8.0-3
- Fixed FTBFS by adding workaround for rebar-related issue #960079

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 03 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.8.0-1
- Ver. 0.8.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 05 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.7.0-1
- Upstream is switched to Basho
- Ver. 0.7.0
- Dropped all Basho's patches

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.6.20100930git58ff962
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.5.20100930git58ff962
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Mar 11 2011 Peter Lemenkov <lemenkov@gmail.com> -  0-0.4.20100930git58ff962
- Added three patches from Basho's fork (required for riak_client)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.3.20100930git58ff962
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct  5 2010 Peter Lemenkov <lemenkov@gmail.com> - 0-0.2.20100930git58ff962
- Fixed License tag

* Thu Sep 30 2010 Peter Lemenkov <lemenkov@gmail.com> - 0-0.1.20100930git58ff962
- Initial package
