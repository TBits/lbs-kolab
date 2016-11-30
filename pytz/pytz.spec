%if 0%{?fedora}
%global with_python3 1
%else
%{!?python2_sitelib: %global python2_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python2_version: %global python2_version %(%{__python} -c "from distutils.sysconfig import get_python_version; print get_python_version()")}
%endif

Name:           pytz
Version:        2015.7
Release:        2%{?dist}
Summary:        World Timezone Definitions for Python

Group:          Development/Languages
License:        MIT
URL:            http://pytz.sourceforge.net/
Source0:        http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
# Patch to use the system supplied zoneinfo files
Patch0:         pytz-zoneinfo.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  pytest
Requires:       tzdata
Provides:       python2-pytz = %{version}-%{release}

%description
pytz brings the Olson tz database into Python. This library allows accurate
and cross platform timezone calculations using Python 2.3 or higher. It
also solves the issue of ambiguous times at the end of daylight savings,
which you can read more about in the Python Library Reference
(datetime.tzinfo).

Almost all (over 540) of the Olson timezones are supported.

%if 0%{?with_python3}
%package -n python3-%{name}
Summary:        World Timezone Definitions for Python
Group:          Development/Languages
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
Requires:       tzdata

%description -n python3-%{name}
pytz brings the Olson tz database into Python. This library allows accurate
and cross platform timezone calculations using Python 2.3 or higher. It
also solves the issue of ambiguous times at the end of daylight savings,
which you can read more about in the Python Library Reference
(datetime.tzinfo).

Almost all (over 540) of the Olson timezones are supported.
%endif

%prep
%setup -q
%patch0 -p1 -b .zoneinfo


%build
%{__python} setup.py build
%if 0%{?with_python3}
%{__python3} setup.py build
%endif # with_python3


%install
%{__python} setup.py install --skip-build --root %{buildroot}
chmod +x %{buildroot}%{python2_sitelib}/pytz/*.py
rm -r %{buildroot}%{python2_sitelib}/pytz/zoneinfo

%if 0%{?with_python3}
%{__python3} setup.py install --skip-build --root %{buildroot}
rm -r %{buildroot}%{python3_sitelib}/pytz/zoneinfo
%endif # with_python3


%check
PYTHONPATH=%{buildroot}%{python2_sitelib} py.test-%{python2_version} -v
%if 0%{?with_python3}
PYTHONPATH=%{buildroot}%{python2_sitelib} py.test-%{python3_version} -v
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%files
%doc CHANGES.txt LICENSE.txt README.txt
%{python2_sitelib}/pytz/
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-pytz
%doc CHANGES.txt LICENSE.txt README.txt
%{python3_sitelib}/pytz/
%{python3_sitelib}/*.egg-info
%endif # with_python3


%changelog
* Tue Nov 03 2015 Robert Kuska <rkuska@redhat.com> - 2015.7-2
- Rebuilt for Python3.5 rebuild

* Mon Oct 26 2015 Orion Poplawski <orion@cora.nwra.com> - 2015.7-1
- Update to 2015.7

* Sun Aug 30 2015 Orion Poplawski <orion@cora.nwra.com> - 2015.4-1
- Update to 2015.4 (bug #1161236)
- Do not ship zoneinfo with python3 package (bug #1251554)
- Run tests

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012d-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012d-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 2012d-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012d-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012d-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan  3 2013 David Malcolm <dmalcolm@redhat.com> - 2012d-3
- remove rhel logic from with_python3 conditional

* Fri Sep 14 2012 Jon Ciesla <limburgher@gmail.com> - 2012d-2
- Use system zoneinfo, BZ 857266.

* Thu Aug 23 2012 Jon Ciesla <limburgher@gmail.com> - 2012d-1
- Latest upstream, python3 support, BZ 851226.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2010h-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2010h-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2010h-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2010h-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jun 28 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 2010h-2
- Define => global

* Tue Apr 27 2010 Jon Ciesla <limb@jcomserv.net> - 2010h-1
- Update to current version, BZ 573252.

* Mon Feb 01 2010 Jon Ciesla <limb@jcomserv.net> - 2009i-7
- Corrected Source0 URL, BZ 560168.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2008i-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2008i-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2008i-4
- Rebuild for Python 2.6

* Tue Nov 18 2008 Jef Spaleta <jspaleta at fedoraproject dot org> 2008i-3
- Apply patch correctly.

* Thu Nov 13 2008 Jef Spaleta <jspaleta at fedoraproject dot org> 2008i-2
- Updated tzdata patch from Petr Machata bug 471014

* Tue Nov 11 2008 Jef Spaleta <jspaleta at fedoraproject dot org> 2008i-1
- Update to latest, now using timezone files provided by tzdata package

* Fri Jan 04 2008 Jef Spaleta <jspaleta@gmail.com> 2006p-3
- Fix for egg-info file creation

* Mon Dec 11 2006 Jef Spaleta <jspaleta@gmail.com> 2006p-2
- Bump for rebuild against python 2.5 and change BR to python-devel accordingly

* Fri Dec  8 2006 Orion Poplawski <orion@cora.nwra.com> 2006p-1
- Update to 2006p

* Thu Sep  7 2006 Orion Poplawski <orion@cora.nwra.com> 2006g-1
- Update to 2006g

* Mon Feb 13 2006 Orion Poplawski <orion@cora.nwra.com> 2005r-2
- Rebuild for gcc/glibc changes

* Tue Jan  3 2006 Orion Poplawski <orion@cora.nwra.com> 2005r-1
- Update to 2005r

* Thu Dec 22 2005 Orion Poplawski <orion@cora.nwra.com> 2005m-1
- Update to 2005m

* Fri Jul 22 2005 Orion Poplawski <orion@cora.nwra.com> 2005i-2
- Remove -O1 from install command

* Tue Jul 05 2005 Orion Poplawski <orion@cora.nwra.com> 2005i-1
- Initial Fedora Extras package