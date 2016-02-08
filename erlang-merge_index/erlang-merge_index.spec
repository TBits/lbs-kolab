%global realname merge_index
%global upstream basho
%global debug_package %{nil}
%global git_tag 6005202
%global patchnumber 0


Name:		erlang-%{realname}
Version:	1.3.0
Release:	5%{?dist}
Summary:	An Erlang library for storing ordered sets on disk
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/merge_index
# wget --content-disposition https://github.com/basho/merge_index/tarball/1.3.0
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz
BuildRequires:	erlang-lager
BuildRequires:	erlang-rebar
# Error:erlang(lists:keyfind/3) in R12B and older
# Error:erlang(os:timestamp/0) in R12B and older
Requires:	erlang-erts%{?_isa} >= R13B
Requires:	erlang-kernel%{?_isa}
Requires:	erlang-lager%{?_isa}
# Error:erlang(queue:member/2) in R12B and older
# Error:erlang(random:seed/1) in R12B and older
Requires:	erlang-stdlib%{?_isa} >= R13B


%description
MergeIndex is an Erlang library for storing ordered sets on disk. It is very
similar to an SSTable (in Google's Bigtable) or an HFile (in Hadoop).

Basho Technologies developed MergeIndex to serve as the underlying index storage
format for Riak Search and the upcoming Secondary Index functionality in Riak.


%prep
%setup -q -n %{upstream}-%{realname}-dd788df


%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,include}
install -p -m 0644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -p -m 0644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 0644 include/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include/


%check
# Requires quickcheck which is proprietary software
# w/o it it just returns ok
rebar eunit skip_deps=true -v


%files
%doc LICENSE Notes.txt README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include/
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/*.hrl


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 10 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.0-1
- Ver. 1.3.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 10 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.1-1
- Ver. 1.2.1

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.0-2
- Verbose rebar invocation
- Restored tests

* Thu May 17 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.0-1
- Ver. 1.1.0

* Fri Sep 16 2011 Peter Lemenkov <lemenkov@gmail.com> - 1.0.0-1
- Initial build
