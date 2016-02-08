%global realname riak_err
%global debug_package %{nil}
%global git_tag b435031


Name:		erlang-%{realname}
Version:	1.0.1
Release:	8%{?dist}
Summary:	Enhanced SASL Error Logger for Riak
Group:		Development/Languages
# The file src/trunc_io.erl is licensed under ERPL
License:	ASL 2.0 and ERPL
URL:		https://github.com/basho/riak_core
# wget --no-check-certificate https://github.com/basho/riak_err/tarball/riak_err-1.0.1
Source0:	basho-%{realname}-%{realname}-%{version}-0-g%{git_tag}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	erlang-erts
BuildRequires:	erlang-eunit
BuildRequires:	erlang-rebar
Requires:	erlang-erts
Requires:	erlang-kernel
Requires:	erlang-sasl
Requires:	erlang-stdlib


%description
Enhanced SASL Error Logger for Riak.


%prep
%setup -q -n basho-%{realname}-%{git_tag}


%build
rebar compile -v


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 644 ebin/%{realname}.app $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 644 ebin/*.beam $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin


%clean
rm -rf $RPM_BUILD_ROOT


%check
rebar eunit


%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/trunc_io.beam


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Feb 25 2011 Peter Lemenkov <lemenkov@gmail.com> - 1.0.1-1
- Ver. 1.0.1 (bugfix release)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.2.20110105git429f757
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Peter Lemenkov <lemenkov@gmail.com> - 1.0.0-0.1.20110105git429f757
- Initial build


