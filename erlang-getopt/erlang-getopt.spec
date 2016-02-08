%global realname getopt
%global upstream jcomellas
%global debug_package %{nil}


Name:		erlang-%{realname}
Version:	0.8.2
Release:	2%{?dist}
Summary:	Erlang module to parse command line arguments using the GNU getopt syntax
Group:		Development/Libraries
License:	BSD
URL:		http://github.com/%{upstream}/%{realname}
%if 0%{?el7}%{?fedora}
VCS:		scm:git:https://github.com/%{upstream}/%{realname}.git
%endif
Source0:	https://github.com/%{upstream}/%{realname}/archive/v%{version}/%{realname}-%{version}.tar.gz
Patch1:		getopt-0001-Fix-edoc-compilation.patch
BuildRequires:	erlang-rebar
Requires:	erlang-erts%{?_isa} >= R13B
Requires:	erlang-stdlib%{?_isa} >= R13B


%description
Command-line parsing module that uses a syntax similar to that of GNU getopt.


%prep
%setup -q -n %{realname}-%{version}
chmod 0644 examples/*.escript
%patch1 -p1 -b .fix_edoc


%build
rebar compile -v
rebar doc -v


%check
# BEWARE rebar needs bootstrapped getopt in case of an API change
rebar eunit -v


%install
install -D -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -D -m 644 ebin/%{realname}.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam


%files
%doc LICENSE.txt README.md examples/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Nov 16 2014 Peter Lemenkov <lemenkov@gmail.com> - 0.8.2-1
- Ver. 0.8.2

* Sun Nov 16 2014 Peter Lemenkov <lemenkov@gmail.com> - 0.8.2-0
- Bootstrap ver. 0.8.2 with disabled tests

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 02 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.7.0-1
- Ver. 0.7.0
- Removed EL5-related stuff

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 21 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.6.0-1
- Ver. 0.6.0

* Thu Oct 11 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.5.2-2
- Rebuild with tests
- Finally fixed tests on EL5

* Thu Oct 11 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.5.2-1
- Ver. 0.5.2

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.4.4-2
- Workaround for EL5's rebar

* Sat Jun 02 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.4.4-1
- Ver. 0.4.4

* Fri Jun 01 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.4.3-2
- Fix building on EPEL-5 (again)
- Enabled tests

* Tue May 15 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.4.3-1
- Ver. 0.4.3

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct  6 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.3-3
- Fix building on EPEL-5

* Tue Oct  5 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.3-2
- Fixed License tag
- Doc-files now have 644 mode

* Thu Sep 30 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.3-1
- Initial package
- Disabled %%check section until rebar will be available

