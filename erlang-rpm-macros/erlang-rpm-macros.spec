Name:		erlang-rpm-macros
Version:	0.2.2
Release:	1%{?dist}
Summary:	Macros for simplifying building of Erlang packages
Group:		Development/Libraries
License:	MIT
URL:		https://github.com/lemenkov/erlang-rpm-macros
%if 0%{?rhel} > 6 || 0%{?fedora}
VCS:		scm:git:https://github.com/lemenkov/erlang-rpm-macros.git
%endif
Source0:	https://github.com/lemenkov/erlang-rpm-macros/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:	noarch
Requires:	rpm-build >= 4.8
# Requires for BEAM parsing
Requires:	python2-pybeam
Requires:	rpm-python


%description
Macros for simplifying building of Erlang packages.


%prep
%setup -q


%build
# Nothing to build


%install
install -d %{buildroot}%{_rpmconfigdir}/fileattrs
install -d %{buildroot}%{_rpmconfigdir}/macros.d
install -p -m 0755 erlang-find-provides.escript %{buildroot}%{_rpmconfigdir}/
install -p -m 0755 erlang-find-provides.py %{buildroot}%{_rpmconfigdir}/
install -p -m 0755 erlang-find-requires.escript %{buildroot}%{_rpmconfigdir}/
install -p -m 0755 erlang-find-requires.py %{buildroot}%{_rpmconfigdir}/
install -p -m 0644 macros.erlang %{buildroot}%{_rpmconfigdir}/macros.d/
install -p -m 0644 erlang.attr %{buildroot}%{_rpmconfigdir}/fileattrs/


%files
%if 0%{?fedora}
%license LICENSE
%else
%doc LICENSE
%endif
%doc README
%{_rpmconfigdir}/erlang-find-provides.escript
%{_rpmconfigdir}/erlang-find-provides.py
%{_rpmconfigdir}/erlang-find-requires.escript
%{_rpmconfigdir}/erlang-find-requires.py
%{_rpmconfigdir}/fileattrs/erlang.attr
%{_rpmconfigdir}/macros.d/macros.erlang
%exclude %{_rpmconfigdir}/*.pyc
%exclude %{_rpmconfigdir}/*.pyo



%changelog
* Thu Mar 10 2016 Peter Lemenkov <lemenkov@gmail.com> - 0.2.2-1
- Ver. 0.2.2

* Mon Mar  7 2016 Peter Lemenkov <lemenkov@gmail.com> - 0.2.1-2
- Allow skippind dependency checking in rebar

* Sun Mar  6 2016 Peter Lemenkov <lemenkov@gmail.com> - 0.2.1-1
- Ver. 0.2.1

* Tue Mar  1 2016 Peter Lemenkov <lemenkov@gmail.com> - 0.2.0-2
- Added missing Requires

* Tue Mar  1 2016 Peter Lemenkov <lemenkov@gmail.com> - 0.2.0-1
- Ver. 0.2.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 13 2014 Peter Lemenkov <lemenkov@gmail.com> - 0.1.4-1
- Ver. 0.1.4
- Dropped support for pre-4.11 rpms (EL7 or Fedora is required)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 31 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.1.3-6
- Cleaning up spec-file

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.1.3-4
- Remove %%config from %%{_sysconfdir}/rpm/macros.*
  (https://fedorahosted.org/fpc/ticket/259).

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 07 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.1.3-1
- Ver. 0.1.3

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 15 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.1.2-2
- Drop explicit Requires: erlang-erts

* Mon Nov 15 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.1.2-1
- Ver. 0.1.2
- Added missing runtime requirements

* Wed Oct 27 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.1.1-1
- Initial build as separate package (splitted off from erlang)
