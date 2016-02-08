%global realname lfe
%global upstream rvirding
%global git_tag 0b728d4 
%global debug_package %{nil}


Name:		erlang-%{realname}
Version:	0.9.2
Release:	1%{?dist}
Summary:	Lisp Flavoured Erlang
Group:		Development/Languages
License:	BSD
URL:		http://github.com/rvirding/lfe
%if 0%{?el7}%{?fedora}
VCS:		scm:git:https://github.com/rvirding/lfe.git
%endif
Source0:	https://github.com/rvirding/lfe/archive/v%{version}/%{realname}-%{version}.tar.gz
BuildRequires:	erlang-rebar
BuildRequires:	pkgconfig
BuildRequires:	emacs
BuildRequires:	emacs-el

Requires:	erlang-compiler%{?_isa}
Requires:	erlang-erts%{?_isa}
Requires:	erlang-kernel%{?_isa}
# Error:erlang(unicode:characters_to_list/1) in R12B and earlier
Requires:	erlang-stdlib%{?_isa} >= R13B


%description
Lisp Flavoured Erlang, is a lisp syntax front-end to the Erlang
compiler. Code produced with it is compatible with "normal" Erlang
code. An LFE evaluator and shell is also included.

%package -n emacs-erlang-lfe
Summary:	Emacs major mode for Lisp Flavoured Erlang
Group:		Applications/Editors
Requires:	%{name} = %{version}-%{release}
Requires:	emacs(bin) >= %{_emacs_version}
BuildArch:	noarch

%description -n emacs-erlang-lfe
This package provides an Emacs major mode to edit Lisp Flavoured Erlang
files.

%package -n emacs-erlang-lfe-el
Summary:	Elisp source files for Lisp Flavoured Erlang under GNU Emacs
Group:		Applications/Editors
Requires:	%{name} = %{version}-%{release}
Requires:	emacs(bin) >= %{_emacs_version}
BuildArch:	noarch

%description -n emacs-erlang-lfe-el
This package contains the elisp source files for Lisp Flavoured Erlang
under GNU Emacs. You do not need to install this package to run
Lisp Flavoured Erlang. Install the emacs-erlang-lfe package to use
Lisp Flavoured Erlang with GNU Emacs.


%prep
%setup -q -n %{realname}-%{version}
iconv -f iso-8859-1 -t UTF-8  examples/core-macros.lfe > examples/core-macros.lfe.utf8
mv  -f examples/core-macros.lfe.utf8 examples/core-macros.lfe


%build
rebar compile -v
emacs -batch -f batch-byte-compile emacs/lfe-mode.el


%install
install -p -m 0644 -D ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -p -m 0644 ebin/%{realname}_*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
mkdir -p %{buildroot}%{_emacs_sitelispdir}
mkdir -p %{buildroot}%{_emacs_sitestartdir}
install -p -m 0644 emacs/lfe-mode.el %{buildroot}%{_emacs_sitelispdir}
install -p -m 0644 emacs/lfe-mode.elc %{buildroot}%{_emacs_sitelispdir}
install -p -m 0644 emacs/lfe-start.el %{buildroot}%{_emacs_sitestartdir}


%check
rm -rf test/visual/test_map_e.erl
rebar skip_deps=true eunit -v


%files
%doc LICENSE README.md doc/ examples/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_*.beam


%files -n emacs-erlang-lfe
%{_emacs_sitestartdir}/lfe-start.el
%{_emacs_sitelispdir}/lfe-mode.elc


%files -n emacs-erlang-lfe-el
%{_emacs_sitelispdir}/lfe-mode.el


%changelog
* Sun Nov 16 2014 Peter Lemenkov <lemenkov@gmail.com> - 0.9.0-2
- Disable debuginfo

* Sun Nov 16 2014 Peter Lemenkov <lemenkov@gmail.com> - 0.9.0-1
- Ver. 0.9.0
- Drop support for EL5

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 11 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.6.2-1
- Ver. 0.6.2 (Backwards API/ABI compatible)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 17 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.6.1-5
- Make building of emacs sub-packages conditional (and disable on EL-5)

* Sun Nov 14 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.6.1-4
- Remove duplicated emacs files from docs

* Sun Oct 31 2010 Tim Niemueller <tim@niemueller.de> - 0.6.1-3
- Added Emacs sub-package
- Fix inconsitent macro usage

* Fri Oct 15 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.6.1-2
- Provide (x)emacs subpackages

* Fri Oct  1 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.6.1-1
- Initial build
