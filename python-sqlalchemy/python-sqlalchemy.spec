%if ! 0%{?rhel} > 5
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

%if 0%{?fedora} > 12
%global with_python3 1
%endif


%global srcname SQLAlchemy

Name:           python-sqlalchemy
Version:        0.8.0
Release:        1%{?dist}
Summary:        Modular and flexible ORM library for python

Group:          Development/Libraries
License:        MIT
URL:            http://www.sqlalchemy.org/
Source0:        http://pypi.python.org/packages/source/S/%{srcname}/%{srcname}-%{version}.tar.gz
Patch0: sqlalchemy-unittest-ordering.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-nose

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-nose
%endif

%description
SQLAlchemy is an Object Relational Mappper (ORM) that provides a flexible,
high-level interface to SQL databases.  Database and domain concepts are
decoupled, allowing both sides maximum flexibility and power. SQLAlchemy
provides a powerful mapping layer that can work as automatically or as manually
as you choose, determining relationships based on foreign keys or letting you
define the join conditions explicitly, to bridge the gap between database and
domain.

This package includes the python 2 version of the module.

%if 0%{?with_python3}
%package -n python3-sqlalchemy
Summary:        Modular and flexible ORM library for python
Group:          Development/Libraries

%description -n python3-sqlalchemy
SQLAlchemy is an Object Relational Mappper (ORM) that provides a flexible,
high-level interface to SQL databases.  Database and domain concepts are
decoupled, allowing both sides maximum flexibility and power. SQLAlchemy
provides a powerful mapping layer that can work as automatically or as manually
as you choose, determining relationships based on foreign keys or letting you
define the join conditions explicitly, to bridge the gap between database and
domain.

This package includes the python 3 version of the module.
%endif # with_python3

# Filter unnecessary dependencies
%global __provides_exclude_from ^(%{python_sitearch}|%{python3_sitearch})/.*\\.so$

%prep
%setup -q -n %{srcname}-0.8.0
%patch0 -p1 -b .ordering

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
CFLAGS="%{optflags}" %{__python} setup.py --with-cextensions build

%if 0%{?with_python3}
pushd %{py3dir}
# Convert tests, examples, source to python3
%{__python3} sa2to3.py --no-diffs -w lib test examples
# Currently the cextension doesn't work with python3
CFLAGS="%{optflags}" %{__python3} setup.py build
popd
%endif

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{python_sitelib}
%{__python} setup.py --with-cextensions install --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
mkdir -p %{buildroot}%{python3_sitelib}
# Currently the cextension doesn't work with python3
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

# remove unnecessary scripts for building documentation
rm -rf doc/build

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.rst LICENSE PKG-INFO CHANGES doc examples
%{python_sitearch}/*

%if 0%{?with_python3}
%files -n python3-sqlalchemy
%defattr(-,root,root,-)
%doc LICENSE PKG-INFO doc examples
%{python3_sitelib}/*
%endif # with_python3

%changelog
* Fri Apr 12 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 0.8.0-1
- Final release of 0.8.0
- Fix for a unittest that assumes order in dicts

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-0.2.b1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov  1 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.8.0-0.1.b1
- Update to 0.8.0 beta

* Mon Aug 13 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7.8-4.20120813hg8535
- Update to a snapshot to fix unittest errors with python-3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 0.7.8-3
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 18 2012 Nils Philippsen <nils@redhat.com> - 0.7.8-1
- Upstream bugfix release

* Tue May 15 2012 Nils Philippsen <nils@redhat.com> - 0.7.7-1
- Upstream bugfix release

* Tue Mar 20 2012 Nils Philippsen <nils@redhat.com> - 0.7.6-1
- Upstream bugfix release

* Mon Jan 30 2012 Nils Philippsen <nils@redhat.com> - 0.7.5-1
- Upstream bugfix release
- package README.rst instead of README as documentation

* Tue Jan 10 2012 Nils Philippsen <nils@redhat.com> - 0.7.3-2
- rebuild for gcc 4.7

* Mon Oct 17 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7.3-1
- Upstream bugfix release

* Mon Aug 1 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7.2-1
- Upstream bugfix release

* Mon Jun 06 2011 Nils Philippsen <nils@redhat.com> - 0.7.1-1
- 0.7.1 Upstream release
- no need to fix examples/dynamic_dict/dynamic_dict.py anymore
- use sqla_nose.py to fix %%check

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.6-1
- 0.6.6 Upstream release

* Fri Dec 3 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.5-1
- 0.6.5 Upstream release

* Wed Sep 29 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.4-2
- Filter out the C extensions from provides

* Tue Sep 07 2010 Luke Macken <lmacken@redhat.com> - 0.6.4-1
- 0.6.4 upstream release

* Mon Aug 23 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.3-1
- 0.6.3 upstream release

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com>
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jun 24 2010 Nils Philippsen <nils@redhat.com> - 0.6.1-1
- 0.6.1 upstream release

* Tue Apr 13 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6-0.4.beta3
- Build beta3

* Fri Mar 19 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6-0.3.beta2
- Build beta2 with cextension

* Sun Mar 7 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6-0.2.beta1
- Build python3 package

* Tue Mar 2 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6-0.1.beta1
- 0.6 beta1 upstream release

* Tue Feb 2 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.5.8-3
- One last cleanup

* Tue Feb 2 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.5.8-2
- just some cleanups to older styles of building packages.

* Mon Feb 1 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.5.8-1
- Upstream bugfix release 0.5.8

* Fri Aug 14 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.5.5-2
- Upstream bugfix release 0.5.5

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-2.p2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.5.4-1.p2
- Upstream bugfix release 0.5.4p2.

* Thu Apr 16 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.5.3-1
- Upstream bugfix release.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.5.2-1
- Update to 0.5.2

* Wed Jan 21 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.5.1-1
- Update to 0.5.1.

* Mon Dec 1 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 0.5-0.1.rc4
- Update to 0.5.0rc4 which works with the new pysqlite
- And update test cases to work with the new pysqlite

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.4.7-2
- Rebuild for Python 2.6

* Sun Jul 27 2008 Toshio Kuratomi <toshio@fedoraproject.org> 0.4.7-1
- Update to 0.4.7.

* Sun Jun 1 2008 Toshio Kuratomi <toshio@fedoraproject.org> 0.4.6-1
- Update to 0.4.6.

* Tue Apr 8 2008 Toshio Kuratomi <toshio@fedoraproject.org> 0.4.5-1
- Update to 0.4.5.

* Fri Feb 22 2008 Toshio Kuratomi <toshio@fedoraproject.org> 0.4.3-1
- Update to 0.4.3.

* Tue Dec 11 2007 Toshio Kuratomi <a.badger@gmail.com> 0.4.2-1.p3
- Update to 0.4.2p3.

* Tue Dec 11 2007 Toshio Kuratomi <a.badger@gmail.com> 0.4.1-1
- Update to 0.4.1.

* Wed Oct 17 2007 Toshio Kuratomi <a.badger@gmail.com> 0.4.0-1
- SQLAlchemy-0.4.0 final
- Run the testsuite

* Wed Oct  3 2007 Luke Macken <lmacken@redhat.com> 0.4.0-0.4.beta6
- SQLAlchemy-0.4.0beta6

* Tue Sep 11 2007 Toshio Kuratomi <a.badger@gmail.com> - 0.4.0-0.4.beta5
- Update to 0.4beta5.

* Fri Sep 06 2007 Toshio Kuratomi <a.badger@gmail.com> - 0.4.0-0.4.beta4
- setuptools has been fixed.

* Fri Aug 31 2007 Toshio Kuratomi <a.badger@gmail.com> - 0.4.0-0.3.beta4
- setuptools seems to be broken WRT having an active and inactive version
  of an egg.  Have to make both versions inactive and manually setup a copy
  that can be started via import. (Necessary for the sqlalchemy0.3 compat
  package.)

* Tue Aug 28 2007 Toshio Kuratomi <a.badger@gmail.com> - 0.4.0-0.2.beta4
- Modify setuptools to handle the -devel subpackage split in F-8.

* Mon Aug 27 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.4.0-0.1.beta4
- Update to 0.4 beta4.

* Tue Jul 24 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.3.10-2
- Remove python-abi Requires.  This is automatic since FC4+.

* Tue Jul 24 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.3.10-1
- Update to new upstream version 0.3.10

* Fri Mar 23 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.3.6-1
- Update to new upstream version 0.3.6

* Sat Mar 10 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.3.5-1
- Update to new upstream version 0.3.5
- Simplify the files listing

* Tue Jan 23 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.3.4-2
- Remember to upload the source tarball to the lookaside cache.

* Tue Jan 23 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.3.4-1
- Update to new upstream version 0.3.4

* Mon Jan 01 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.3.3-1
- Update to new upstream version 0.3.3

* Sat Dec 09 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.3.1-2
- Bump and rebuild for python 2.5 on devel.
- BuildRequire: python-devel as a header is missing otherwise.

* Fri Nov 24 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.3.1-1
- Update to new upstream version 0.3.1

* Sat Sep 16 2006 Shahms E. King <shahms@shahms.com> 0.2.7-2
- Rebuild for FC6

* Thu Aug 17 2006 Shahms E. King <shahms@shahms.com> 0.2.7-1
- Update to new upstream version

* Fri Aug 11 2006 Shahms E. King <shahms@shahms.com> 0.2.6-2
- Include, don't ghost .pyo files per new guidelines

* Tue Aug 08 2006 Shahms E. King <shahms@shahms.com> 0.2.6-1
- Update to new upstream version

* Fri Jul 07 2006 Shahms E. King <shahms@shahms.com> 0.2.4-1
- Update to new upstream version

* Mon Jun 26 2006 Shahms E. King <shahms@shahms.com> 0.2.3-1
- Update to new upstream version

* Wed May 31 2006 Shahms E. King <shahms@shahms.com> 0.2.1-1
- Update to new upstream version
