
%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname meck
%global upstream eproxus
# Techincally, we're noarch; but erlang whose directories we install into is not.
%global debug_package %{nil}
%global git_tag dde7590
%global patchnumber 0


Name:           erlang-%{realname}
Version:        0.8.2
Release:        7%{?dist}
Summary:        A mocking library for Erlang
Group:          Development/Libraries
License:        ASL 2.0
URL:            http://eproxus.github.com/meck/
# wget --content-disposition https://github.com/eproxus/meck/tarball/0.7.2
Source0:        %{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz

Patch1:         erlang-meck-0.8.2-var-from-case.patch

BuildRequires:  erlang-rebar
BuildRequires:  erlang-hamcrest

Requires:       erlang-compiler%{?_isa}
Requires:       erlang-erts%{?_isa}
Requires:       erlang-kernel%{?_isa}
Requires:       erlang-stdlib%{?_isa}
# Error:erlang(cover:compile_beam/2)
# Error:erlang(cover:get_term/1)
# Error:erlang(cover:write/2)
Requires:       erlang-tools%{?_isa}

%description
With meck you can easily mock modules in Erlang. Since meck is intended to be
used in testing, you can also perform some basic validations on the mocked
modules, such as making sure no function is called in a way it should not.

%prep
%setup -q -n %{upstream}-%{realname}-3599670
%patch1 -p1

%build
rebar compile -v

%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 rebar.config %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/

%check
rebar -C test.config skip_deps=true eunit -v || :

%files
%doc LICENSE README.md NOTICE
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/rebar.config

%changelog
* Fri May 15 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.8.2-1
- Check in 0.8.2

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 28 2014 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 0.7.2-5
- Fix build

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 02 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.7.2-3
- Remove tests parametrized modules - they are no longer supported
- Drop support for EL5

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 05 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.7.2-1
- Ver. 0.7.2

* Wed Aug 15 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.7.1-4
- Fix for EL5

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 17 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.7.1-2
- Pick up all missing requires

* Mon Feb 13 2012 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 0.7.1-1
- Rebase
- Review fixes (Peter Lemenkov, #705773)

* Wed May 18 2011 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 0.5-1
- Initial packaging
