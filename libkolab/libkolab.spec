# Needed for opensuse build system
%if 0%{?opensuse_bs}
#!BuildIgnore:  fedora-logos-httpd
#!BuildIgnore:  httpd
%endif

%if 0%{?suse_version}
%global php php5
%{!?php_inidir: %global php_inidir %{_sysconfdir}/php5/conf.d/}
%{!?php_extdir: %global php_extdir %{_libdir}/php5/extensions}
%else
%global php php
%{!?php_inidir: %global php_inidir %{_sysconfdir}/php.d/}
%{!?php_extdir: %global php_extdir %{_libdir}/php/modules}
%endif
%{!?php_apiver: %global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)}
 
# Filter out private python and php libs. Does not work on EPEL5,
# therefor we use it conditionally
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_provides_in %{php_extdir}/.*\.so$
%filter_setup
}

%if 0%{?suse_version}
Name:           libkolab0
%else
Name:           libkolab
%endif

Version:        0.6.0
Release:        1%{?dist}
Summary:        Kolab Object Handling Library

License:        LGPLv3+
URL:            http://git.kolab.org/libkolab

Source0:        http://git.kolab.org/%{name}/snapshot/libkolab-%{version}.tar.gz

Patch0001:      0001-Add-support-for-exceptions.patch
Patch0002:      0002-Support-for-THISANDFUTURE.patch
Patch0003:      0003-Move-QT_DECLARE_METADATA-logic-to-cmake.patch

BuildRequires:  cmake
%if 0%{?rhel} > 6 || 0%{?fedora} > 16
BuildRequires:  kdepimlibs-devel >= 4.9
%else
# Note: available within kolabsys.com infrastructure only, as being (essentially) a
# fork of various kde 4.9 libraries that depend on kde*, and that have no place in el6.
BuildRequires:  libcalendaring-devel >= 4.9
%endif
BuildRequires:  libcurl-devel
BuildRequires:  libkolabxml-devel >= 1.0
BuildRequires:  php >= 5.3
BuildRequires:  php-devel >= 5.3
BuildRequires:  python-devel
%if 0%{?suse_version}
BuildRequires:  qt-devel
%else
BuildRequires:  qt4-devel
%endif
Provides:       libkolab%{?_isa} = %{version}

%description
The libkolab library is an advanced library to  handle Kolab objects.

%if 0%{?suse_version}
%package -n libkolab-devel
%else
%package devel
%endif
Summary:        Kolab library development headers
Requires:       libkolab%{?_isa} = %{version}
%if 0%{?rhel} > 6 || 0%{?fedora} > 16
BuildRequires:  kdepimlibs-devel >= 4.9
%else
# Note: available within kolabsys.com infrastructure only, as being (essentially) a
# fork of various kde 4.9 libraries that depend on kde*, and that have no place in el6.
BuildRequires:  libcalendaring-devel >= 4.9
%endif
Requires:       libkolabxml-devel >= 1.0
Requires:       php-devel
Requires:       pkgconfig
Requires:       python-devel


%if 0%{?suse_version}
%description -n libkolab-devel
%else
%description devel
%endif
Development headers for the Kolab object libraries.

%package -n php-kolab
Summary:        PHP Bindings for libkolab
Group:          System Environment/Libraries
Requires:       libkolab%{?_isa} = %{version}
%if 0%{?rhel} > 5 || 0%{?fedora} > 15
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
%else
Requires:       php-api = %{php_apiver}
%endif
%if 0%{?suse_version}
Obsoletes:      php-%{name} < %{version}
Provides:       php-%{name} = %{version}
%endif

%description -n php-kolab
PHP Bindings for libkolab

%package -n python-kolab
Summary:        Python bindings for libkolab
Group:          System Environment/Libraries
Requires:       libkolab%{?_isa} = %{version}
Requires:       python-kolabformat >= 1.0.0
%if 0%{?suse_version}
Obsoletes:      python-%{name} < %{version}
Provides:       python-%{name} = %{version}
%endif

%description -n python-kolab
Python bindings for libkolab

%prep
%setup -q -n libkolab-%{version}

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1

%build
rm -rf build
mkdir -p build
pushd build
%if 0%{?suse_version}
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ;
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ;
FFLAGS="${FFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FFLAGS ;
FCFLAGS="${FCFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FCFLAGS ;
%{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;}
cmake \
    -DCMAKE_C_FLAGS_RELEASE:STRING="-DNDEBUG" \
    -DCMAKE_CXX_FLAGS_RELEASE:STRING="-DNDEBUG" \
    -DCMAKE_Fortran_FLAGS_RELEASE:STRING="-DNDEBUG" \
    -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
    -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
    -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
    -DLIB_INSTALL_DIR:PATH=%{_libdir} \
    -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
    -DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \
%if "%{?_lib}" == "lib64"
    %{?_cmake_lib_suffix64} \
%endif
    -DBUILD_SHARED_LIBS:BOOL=ON \
%else
%cmake \
%endif
    -DBoost_NO_BOOST_CMAKE=TRUE \
    -Wno-fatal-errors -Wno-errors \
    -DINCLUDE_INSTALL_DIR=%{_includedir} \
%if 0%{?rhel} < 7 && 0%{?fedora} < 17
    -DUSE_LIBCALENDARING=ON \
%endif
    -DPHP_BINDINGS=ON \
    -DPHP_INSTALL_DIR=%{php_extdir} \
    -DPYTHON_BINDINGS=ON \
    -DPYTHON_INSTALL_DIR=%{python_sitearch} \
    ..
make
popd

%install
rm -rf %{buildroot}
pushd build
make install DESTDIR=%{buildroot}
popd

mkdir -p %{buildroot}/%{_datadir}/%{php}
mv %{buildroot}/%{php_extdir}/*.php %{buildroot}/%{_datadir}/%{php}/.

mkdir -p %{buildroot}/%{php_inidir}
cat >%{buildroot}/%{php_inidir}/kolab.ini <<EOF
; Kolab libraries
extension=kolabobject.so
extension=kolabshared.so
extension=kolabcalendaring.so
extension=kolabicalendar.so
EOF

# Workaround for #2050
cat >%{buildroot}/%{php_inidir}/kolabdummy.ini <<EOF
; Kolab libraries
extension=dummy.so
EOF


touch %{buildroot}/%{python_sitearch}/kolab/__init__.py

%check
pushd build/tests
./benchmarktest || :
./calendaringtest || :
./formattest || :
./freebusytest || :
./icalendartest || :
./kcalconversiontest || :
./upgradetest || :
popd

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/libkolab.so.0
%{_libdir}/libkolab.so.%{version}

%if 0%{?suse_version}
%files -n libkolab-devel
%else
%files devel
%endif
%{_libdir}/libkolab.so
%{_libdir}/cmake/Libkolab
%{_includedir}/kolab

%files -n php-kolab
%config(noreplace) %{php_inidir}/kolab.ini
%config(noreplace) %{php_inidir}/kolabdummy.ini
%{_datadir}/%{php}/dummy.php
%{php_extdir}/dummy.so
%{_datadir}/%{php}/kolabcalendaring.php
%{php_extdir}/kolabcalendaring.so
%{_datadir}/%{php}/kolabicalendar.php
%{php_extdir}/kolabicalendar.so
%{_datadir}/%{php}/kolabobject.php
%{php_extdir}/kolabobject.so
%{_datadir}/%{php}/kolabshared.php
%{php_extdir}/kolabshared.so
%if 0%{?suse_version}
%dir %{php_inidir}
%dir %{_datadir}/%{php}
%dir %{_libdir}/%{php}
%dir %{php_extdir}
%endif

%files -n python-kolab
%dir %{python_sitearch}/kolab/
%{python_sitearch}/kolab/__init__.py*
%{python_sitearch}/kolab/_calendaring.so
%{python_sitearch}/kolab/calendaring.py*
%{python_sitearch}/kolab/_icalendar.so
%{python_sitearch}/kolab/icalendar.py*
%{python_sitearch}/kolab/_kolabobject.so*
%{python_sitearch}/kolab/kolabobject.py*
%{python_sitearch}/kolab/_shared.so*
%{python_sitearch}/kolab/shared.py*

%changelog
* Sun Feb 15 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.6.0-1
- Update to version 0.6.0

* Sun Jan 11 2015 Christoph Wickert <wickert@kolabsys.com> - 0.5.3-4
- Load dummy.so through separate ini file (#2050)

* Wed Dec 10 2014 Christoph Wickert <wickert@kolabsys.com> - 0.5.3-3
- Actually apply patch to build the dummy plugin (#2050)

* Tue Dec 09 2014 Christoph Wickert <wickert@kolabsys.com> - 0.5.3-2
- Add dummy plugin to workaround httpd reload issue (#2050)

* Tue Aug 26 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.5.3-1
- New upstream release 0.5.3

* Mon Oct 14 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.5.0-1
- New upstream release

* Thu May 23 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.5-0.2
- GIT snapshot

* Thu Apr 11 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.4.2-1
- New upstream version

* Wed Jan  9 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.4.1-1
- Update version to 0.4.1

* Tue Nov 20 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.4-0.1
- New upstream release
- Correct php.d/kolab.ini

* Wed Aug 15 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3.1-3
- Fix build (patch1)
- Merge back with Fedora,
- Rebuilt for boost (Christoph Wickert, 0.3-10)

* Wed Aug  8 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3.1-1
- New upstream version 0.3.1
- Correct locations and naming of PHP bindings modules

* Thu Aug  2 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3-9
- New snapshot
- Ship PHP and Python bindings
- Conditionally build with libcalendaring
- Execute tests
- Correct installation directory for headers

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3-5
- Fix some review issues (#833853)
- Rebuild after some packaging fixes (4)

* Sat Jun  9 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3-3
- Check in latest snapshot

* Sat May 12 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3-1
- Snapshot version after buildsystem changes

* Wed May  2 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.2.0-1
- First package
