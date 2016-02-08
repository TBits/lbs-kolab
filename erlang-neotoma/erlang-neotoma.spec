%global realname neotoma
%global upstream seancribbs
%global debug_package %{nil}


Name:		erlang-%{realname}
Version:	1.7.2
Release:	1%{?dist}
Summary:	Erlang library and packrat parser-generator for parsing expression grammars
Group:		Development/Languages
License:	MIT
URL:		http://github.com/%{upstream}/%{realname}
%if 0%{?el7}%{?fedora}
VCS:		scm:git:https://github.com/%{upstream}/%{realname}.git
%endif
Source0:	https://github.com/%{upstream}/%{realname}/archive/%{version}/%{realname}-%{version}.tar.gz
BuildRequires:	erlang-rebar
# ets:insert/2 ( >= R12B-5 )
# ets:insert_new/2 ( >= R12B-5 )
# ets:lookup/2 ( >= R12B-5 )
# ets:new/2 ( >= R12B-5 )
# re:compile/1 ( >= R12B-5 )
# re:run/2 ( >= R12B-5 )
Requires:	erlang-erts%{?_isa} >= R12B-5
Requires:	erlang-kernel%{?_isa}
# re:replace/4 ( >= R12B-5 )
# string:join/2 ( >= R12B-5 )
# unicode:characters_to_list/1 ( >= R13B )
Requires:	erlang-stdlib%{?_isa} >= R13B


%description
Erlang library and packrat parser-generator for parsing expression grammars.


%prep
%setup -q -n %{realname}-%{version}
sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src


%build
rebar compile -v


%install
install -p -m 0644 -D ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -p -m 0644 ebin/%{realname}.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 0644 ebin/%{realname}_parse.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 0644 -D priv/peg_includes.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/peg_includes.hrl
install -p -m 0644 priv/neotoma_parse.peg %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv


%check
rebar eunit -v


%files
%doc extra/ LICENSE README.textile
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_parse.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/peg_includes.hrl
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/neotoma_parse.peg


%changelog
* Sun Nov 16 2014 Peter Lemenkov <lemenkov@gmail.com> - 1.7.2-1
- Ver. 1.7.0

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 02 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.6.0-1
- Ver. 1.6.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 11 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.5.1-1
- Ver. 1.5.1

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Mar 26 2011 Peter Lemenkov <lemenkov@gmail.com> - 1.5-1
- Ver. 1.5
- Requires R13B or higher
- BuildRequires rebar

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 28 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.4-2
- Ensure consistency in macro usage

* Fri Oct  1 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.4-1
- Initial build
