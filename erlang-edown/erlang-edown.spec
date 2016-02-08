%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname edown
%global debug_package %{nil}


Name:		erlang-%{realname}
Version:	0.7
Release:	1%{?dist}
Summary:	EDoc extension for generating Github-flavored Markdown
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/esl/edown
%if 0%{?el7}%{?fedora}
VCS:		scm:git:https://github.com/uwiger/edown.git
%endif
Source0:	https://github.com/uwiger/edown/archive/%{version}/%{realname}-%{version}.tar.gz
#BuildRequires:	erlang-edoc
BuildRequires:	erlang-rebar
Requires:	erlang-edoc%{?_isa}
Requires:	erlang-erts%{?_isa}
Requires:	erlang-kernel%{?_isa}
Requires:	erlang-stdlib%{?_isa}
Requires:	erlang-xmerl%{?_isa}


%description
EDoc extension for generating Github-flavored Markdown.


%prep
%setup -q -n %{realname}-%{version}
sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src


%build
rebar compile -v
rebar doc -v


%install
install -p -m 0644 -D ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -p -m 0644 ebin/%{realname}_*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin


%files
%doc NOTICE README.md doc/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_*.beam


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Nov 16 2014 Peter Lemenkov <lemenkov@gmail.com> - 0.4-1
- Ver. 0.4

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 12 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.3.1-1
- Ver. 0.3.1

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 01 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.3.0-1
- Ver. 0.3.0
- Fixed building on EL5

* Mon May 28 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.2.4-2
- Use system-wide rebar

* Fri Sep 16 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.2.4-1
- Ver. 0.2.4
