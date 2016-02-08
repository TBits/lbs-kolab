%global realname sext
%global upstream uwiger
%global debug_package %{nil}
%global git_tag 10529f0
%global patchnumber 0


Name:		erlang-%{realname}
Version:	1.1
Release:	5%{?dist}
Summary:	Sortable Erlang Term Serialization
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/uwiger/sext
# wget --content-disposition https://github.com/uwiger/sext/tarball/1.1
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz
# Fedora/EPEL-specific
Patch1:		erlang-sext-0001-Adjust-version-in-.app-file.patch
BuildRequires:	erlang-rebar
BuildRequires:	erlang-edown
Requires:	erlang-erts%{?_isa}
# Requires only for R12B but doesn't harm anyone on higher versions
Requires:	erlang-kernel%{?_isa}
Requires:	erlang-stdlib%{?_isa}


%description
A sortable serialization library This library offers a serialization format
(a la term_to_binary()) that preserves the Erlang term order.


%prep
%setup -q -n %{upstream}-%{realname}-%{git_tag}
%patch1 -p1 -b .fix_ver


%build
rebar compile -v


%install
install -p -m 0644 -D ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -p -m 0644 ebin/%{realname}.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin


%check
rebar eunit skip_deps=true -v


%files
%doc LICENSE NOTICE README.md examples/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 10 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.1-1
- Ver. 1.1 (Bugfix release)

* Wed Mar 06 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.0-1
- Ver. 1.0
- Removed few Fedora/EPEL-specific patches (no longer required)
- Drop support for EL5

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 11 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.5.2-1
- Ver. 0.5.2 (backwards API/ABI compatible)

* Sun Aug 19 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.5-1
- Ver. 0.5 (backwards API/ABI compatible)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 28 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.4.1-2
- Kill unneeded requires - erlang-eunit

* Thu May 17 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.4.1-1
- Initial build
