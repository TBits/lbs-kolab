%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname rebar
%global upstream rebar
%global debug_package %{nil}
%global git_tag e9f62c4
%global patchnumber 0

# Set this to true when starting a rebuild of the whole erlang stack. There's
# a cyclical dependency between erlang-rebar and erlang-getopt so this package
# (rebar) needs to get built first in bootstrap mode.
%global bootstrap 1

Name:           erlang-%{realname}
Version:        2.5.1
Release:        1%{?dist}
Summary:        Erlang Build Tools
Group:          Development/Tools
License:        MIT
URL:            https://github.com/rebar/rebar
# wget --content-disposition https://github.com/rebar/rebar/tarball/2.5.1
Source0:        %{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz
Source1:        rebar.escript

Patch1:         0001-Don-t-load-templates-from-the-bundle.patch

%if 0%{?bootstrap} < 1
Patch2:         0002-Unbundle-mustache.patch
Patch3:         0003-Unbundle-getopt.patch
%endif

Patch4:         0004-Allow-discarding-building-ports.patch
Patch5:         0005-Check-system-wide-libdir-in-case-of-source-based-dep.patch
Patch6:         0006-Remove-any-traces-of-long-time-obsolete-escript-fold.patch
Patch7:         0007-Remove-abnfc-compiler-support-n-a-in-Fedora-EPEL.patch

%if 0%{?bootstrap} < 1
BuildRequires:  erlang-rebar >= 0.1
%else
BuildRequires:  erlang
%endif

%if 0%{?bootstrap} < 1
Requires:       erlang-erlydtl%{?_isa}
Requires:       erlang-lfe%{?_isa}
Requires:       erlang-neotoma%{?_isa}
Requires:       erlang-protobuffs%{?_isa}
%endif

# FIXME wip
#Requires:       erlang-abnfc%{?_isa}
Requires:       erlang-asn1%{?_isa}
Requires:       erlang-common_test%{?_isa}
Requires:       erlang-compiler%{?_isa}
Requires:       erlang-crypto%{?_isa}
# FIXME does it still needed?
Requires:       erlang-dialyzer%{?_isa}
Requires:       erlang-edoc%{?_isa}
Requires:       erlang-erts%{?_isa}
# Requires for port compiling - no direct references in Rebar's src/*.erl files
Requires:       erlang-erl_interface%{?_isa}
# Autochecker picks up a missing dependency in R16 -
# eunit_test:function_wrapper/2.  This function was removed in R16, and rebar
# contains a workaround for that. So no need to worry about that.
Requires:       erlang-eunit%{?_isa}
Requires:       erlang-kernel%{?_isa}
Requires:       erlang-parsetools%{?_isa}
Requires:       erlang-reltool%{?_isa}
Requires:       erlang-sasl%{?_isa}
Requires:       erlang-snmp%{?_isa}
Requires:       erlang-stdlib%{?_isa}
Requires:       erlang-syntax_tools%{?_isa}
Requires:       erlang-tools%{?_isa}
Provides:       %{realname} = %{version}-%{release}
%if 0%{?bootstrap} < 1
Requires:       erlang-getopt%{?_isa}
Requires:       erlang-mustache%{?_isa}
%endif

%description
Erlang Build Tools.

%prep
%setup -q -n %{upstream}-%{realname}-57ea1c5
%patch1 -p1

%if 0%{?bootstrap} < 1
%patch2 -p1
%patch3 -p1
%endif

%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1


%build
%if 0%{?bootstrap} < 1
rebar compile -v
%else
./bootstrap
./rebar compile -v
%endif


%install
install -D -p -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/rebar
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include
install -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 include/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include
cp -a priv %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/


%check
#rebar eunit -v


%files
%doc LICENSE NOTES.org README.md THANKS rebar.config.sample
%{_bindir}/rebar
%{_libdir}/erlang/lib/%{realname}-%{version}

%changelog
* Mon May 18 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.5.1-1
- Use the upstream version of rebar

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-0.9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-0.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 8 2014 Sam Kottler <skottler@fedoraproject.org> - 2.1.0-0.7
- Add bootstrap variable and necessary conditionals for building without external getopt

* Sun Sep 01 2013 Peter Lemenkov <lemenkov@gmail.com> - 2.1.0-0.5
- Added missing runtime requirements

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 12 2013 Peter Lemenkov <lemenkov@gmail.com> - 2.1.0-0.4
- backported fix for ErlyDTL templates compilation

* Wed Mar 06 2013 Peter Lemenkov <lemenkov@gmail.com> - 2.1.0-0.3
- Don't bootstrap anymore - use rebar for building rebar

* Sun Mar 03 2013 Peter Lemenkov <lemenkov@gmail.com> - 2.1.0-0.2
- Backported fix for suppress building *.so libraries everytime

* Sat Mar 02 2013 Peter Lemenkov <lemenkov@gmail.com> - 2.1.0-0.1
- Ver. 2.1.0-pre
- Remove R12B-related patches (EL5-related)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 18 2012 Peter Lemenkov <lemenkov@gmail.com> - 2.0.0-3
- Fix templates

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 05 2012 Peter Lemenkov <lemenkov@gmail.com> - 2.0.0-1
- Ver. 2.0.0

* Tue May 22 2012 Peter Lemenkov <lemenkov@gmail.com> - 2-9.20120514git635d1a9
- Fix building in EL6 and Fedora

* Mon May 21 2012 Peter Lemenkov <lemenkov@gmail.com> - 2-8.20120514git635d1a9
- Explicitly list erlang-erl_interface as a dependency
- Fixed EPEL5 dependencies

* Sun May 20 2012 Peter Lemenkov <lemenkov@gmail.com> - 2-7.20120514git635d1a9
- Enable building on EL5 (remove erlydtl-related stuff on el5)
- Remove abnfc-related stff until we package it

* Wed May 16 2012 Peter Lemenkov <lemenkov@gmail.com> - 2-6.20120514git635d1a9
- Updated to the latest git snapshot

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2-5.20101120git90058c7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2-4.20101120git90058c7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 22 2010 Peter Lemenkov <lemenkov@gmail.com> - 2-3.20101120git90058c7
- Added missing buildrequires

* Sat Nov 20 2010 Peter Lemenkov <lemenkov@gmail.com> - 2-2.20101120git90058c7
- Removed bundled mustache and getopt
- Fixed license tag
- Removed wrong license text from package
- Simplified %%files section
- Fixed links (project was moved to GitHub)
- Changed versioning scheme (post-release)

* Sun Sep  5 2010 Peter Lemenkov <lemenkov@gmail.com> - 2-1
- Initial build

