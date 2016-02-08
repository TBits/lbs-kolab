%global realname bear
%global upstream boundary
%global debug_package %{nil}
%global git_tag 3fd09d1
%global patchnumber 0


Name:		erlang-%{realname}
Version:	0.1.3
Release:	5%{?dist}
Summary:	A set of statistics functions for erlang
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/boundary/bear
# wget --content-disposition https://github.com/boundary/bear/tarball/0.1.3
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz
BuildRequires:	erlang-rebar
# Error:erlang(erlang:max/2) in R12B and below
# Error:erlang(erlang:min/2) in R12B and below
Requires:	erlang-erts%{?_isa} >= R13B
Requires:	erlang-stdlib%{?_isa}


%description
A set of statistics functions for Erlang. Currently bear is focused on use
inside the Folsom Erlang metrics library but all of these functions are generic
and useful in other situations.


%prep
%setup -q -n %{upstream}-%{realname}-%{git_tag}
sed -i -e "s,git,\"0.1.3\",g" src/bear.app.src


%build
rebar compile -v


%install
install -D -m 644 ebin/%{realname}.app $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -m 644 ebin/%{realname}.beam $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/


%check
# No tests currently
#rebar eunit -v


%files
%doc LICENSE README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 03 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.1.3-1
- Ver. 0.1.3 (Backwards API/ABI compatible release)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 21 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.1.2-1
- Ver. 0.1.2 (API/ABI compatible bugfix release)

* Sun Sep 02 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.1.1-1
- Initial build
