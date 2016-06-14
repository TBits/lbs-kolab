%global realname lfe
%global upstream rvirding


Name:		erlang-%{realname}
Version:	1.0
Release:	2%{?dist}
Summary:	Lisp Flavoured Erlang
Group:		Development/Languages
License:	BSD
URL:		https://github.com/%{upstream}/%{realname}
%if 0%{?el7}%{?fedora}
VCS:		scm:git:https://github.com/%{upstream}/%{realname}.git
%endif
Source0:	https://github.com/%{upstream}/%{realname}/archive/%{version}/%{realname}-%{version}.tar.gz

BuildRequires:	erlang-rebar >= 2.6.1
BuildRequires:	pkgconfig
BuildRequires:	emacs
BuildRequires:	emacs-el
%{?__erlang_drv_version:Requires: %{__erlang_drv_version}}


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
ERL_LIBS=. %{rebar_compile}
emacs -L emacs/ -batch -f batch-byte-compile emacs/inferior-lfe.el emacs/lfe-mode.el emacs/lfe-indent.el


%install
install -m 0755 -d %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{bin,ebin,priv}
install -p -m 0755 -D ebin/* %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -p -m 0755 -D bin/*  %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/bin/
install -p -m 0755 priv/%{realname}_drv.so %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/
install -m 0755 -d %{buildroot}/%{_bindir}
ln -s %{_libdir}/erlang/lib/%{realname}-%{version}/bin/{lfe,lfec,lfescript} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_emacs_sitelispdir}
mkdir -p %{buildroot}%{_emacs_sitestartdir}
install -p -m 0644 emacs/inferior-lfe.el %{buildroot}%{_emacs_sitelispdir}
install -p -m 0644 emacs/inferior-lfe.elc %{buildroot}%{_emacs_sitelispdir}
install -p -m 0644 emacs/lfe-mode.el %{buildroot}%{_emacs_sitelispdir}
install -p -m 0644 emacs/lfe-mode.elc %{buildroot}%{_emacs_sitelispdir}
install -p -m 0644 emacs/lfe-indent.el %{buildroot}%{_emacs_sitelispdir}
install -p -m 0644 emacs/lfe-indent.elc %{buildroot}%{_emacs_sitelispdir}
install -p -m 0644 emacs/lfe-start.el %{buildroot}%{_emacs_sitestartdir}


%check
rebar eunit -vv


%files
%if 0%{?fedora}
%license LICENSE
%else
%doc LICENSE
%endif
%doc README.md doc/ examples/
%{_bindir}/lfe
%{_bindir}/lfec
%{_bindir}/lfescript
%{_erllibdir}/%{realname}-%{version}


%files -n emacs-erlang-lfe
%{_emacs_sitestartdir}/lfe-start.el
%{_emacs_sitelispdir}/inferior-lfe.elc
%{_emacs_sitelispdir}/lfe-mode.elc
%{_emacs_sitelispdir}/lfe-indent.elc


%files -n emacs-erlang-lfe-el
%{_emacs_sitelispdir}/inferior-lfe.el
%{_emacs_sitelispdir}/lfe-mode.el
%{_emacs_sitelispdir}/lfe-indent.el


%changelog
* Thu Mar 17 2016 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.0-1
- Version 1.0

* Tue Mar  1 2016 Peter Lemenkov <lemenkov@gmail.com> - 0.10.1-2
- Install CLI tools as well

* Tue Mar  1 2016 Peter Lemenkov <lemenkov@gmail.com> - 0.10.1-1
- Ver. 0.10.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

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
