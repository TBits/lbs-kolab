
%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname poolboy
%global upstream devinus
%global debug_package %{nil}
%global git_tag fa87a6e
%global patchnumber 0


Name:		erlang-%{realname}
Version:	1.4.2
Release:	1%{?dist}
Summary:	A hunky Erlang worker pool factory
Group:		Development/Languages
License:	Public Domain or ASL 2.0
URL:		https://github.com/devinus/poolboy
# wget --content-disposition https://github.com/devinus/poolboy/tarball/1.4.2
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	erlang-rebar
# Error:erlang(os:timestamp/0) - in R12B
Requires:	erlang-erts%{?_isa} >= R13B
# Error:erlang(queue:member/2 - in R12B
Requires:	erlang-stdlib%{?_isa} >= R13B


%description
A hunky Erlang worker pool factory.


%prep
%setup -q -n %{upstream}-%{realname}-%{git_tag}


%build
rebar compile -v


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
install -p -m 0644 -D ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -p -m 0644 ebin/%{realname}.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 0644 ebin/%{realname}_sup.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 0644 ebin/%{realname}_worker.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin


%clean
rm -rf %{buildroot}


%check
rebar eunit -v


%files
%doc LICENSE README.md UNLICENSE
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_sup.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_worker.beam


%changelog
* Fri May 15 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.4.2-1
- Check in 1.4.2

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 11 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.9.1-1
- Ver. 0.9.1

* Wed Oct 10 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.8.1-1
- Ver. 0.8.1

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.7.0-2
- Consistently use macros
- More verbose rebar operation

* Tue May 15 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.7.0-1
- Ver. 0.7.0

* Fri Sep 16 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.3-1.git0514787
- Initial build
