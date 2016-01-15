%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname lager
%global upstream basho
%global debug_package %{nil}

Name:           erlang-%{realname}
Version:        2.1.0
Release:        1%{?dist}
Summary:        A logging framework for Erlang/OTP
Group:          Development/Languages
License:        ASL 2.0
URL:            http://github.com/%{upstream}/%{realname}
%if 0%{?el7}%{?fedora}
VCS:            scm:git:https://github.com/%{upstream}/%{realname}.git
%endif
Source0:        https://github.com/%{upstream}/%{realname}/archive/%{version}/%{realname}-%{version}.tar.gz

Patch1:         lager-2.1.0-tmpfs.patch
Patch2:         lager-2.1.0-test-noproc.patch

BuildRequires:  erlang-rebar
BuildRequires:  erlang-goldrush >= 0.1.6
Requires:       erlang-compiler%{?_isa}
# Error:erlang(erlang:max/2) in R12B and below
# Error:erlang(erlang:min/2) in R12B and below
# Error:erlang(lists:keyfind/3) in R12B and below
# Error:erlang(os:timestamp/0) in R12B and below
Requires:       erlang-erts%{?_isa} >= R13B
Requires:       erlang-goldrush%{?_isa} >= 0.1.6
# Error:erlang(file:datasync/1) in R13B and below
Requires:       erlang-kernel%{?_isa} >= R14B
# Error:erlang(unicode:characters_to_list/1) in R12B and below
Requires:       erlang-stdlib%{?_isa} >= R13B
Requires:       erlang-syntax_tools%{?_isa}

%description
Lager (as in the beer) is a logging framework for Erlang. Its purpose is to
provide a more traditional way to perform logging in an erlang application that
plays nicely with traditional UNIX logging tools like logrotate and syslog.


%prep
%setup -q -n %{realname}-%{version}
%patch1 -p1
%patch2 -p1

%build
rebar compile -v

%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include
install -p -m 0644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -p -m 0644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 0644 include/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include/
install -p -m 0644 rebar.config %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/

%check
rebar skip_deps=true eunit -v


%files
%doc LICENSE README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/*.hrl
%{_libdir}/erlang/lib/%{realname}-%{version}/rebar.config

%changelog
* Fri May 15 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.1.0-1
- Check in 2.1.0

* Mon Nov 17 2014 Peter Lemenkov <lemenkov@gmail.com> - 1.2.2-5
- Fixed FTBFS (see rhbz #1106221)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 10 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.2.2-1
- Ver. 1.2.2 (API-compatible bugfix release)
- Drop EL5 support from spec-file

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 10 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.1-1
- Ver. 1.2.1 (fixes rhbz #854561)

* Wed Sep 05 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.0-1
- Ver. 1.2.0 (API/ABI compatible)
- Dropped upstreamed patches

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.0.0-2
- Consistently use macros
- Restored BuildRoot in case of EL5

* Fri May 18 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.0.0-1
- Ver. 1.0.0

* Fri Sep 16 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.9.2-1
- Ver. 0.9.2
