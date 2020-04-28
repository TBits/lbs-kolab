Name:           leveldb
Version:        2.0.7
Release:        1.39%{?dist}.kolab_wf
Summary:        A fast and lightweight key/value database library by Google
Group:          Applications/Databases
License:        BSD
URL:            http://code.google.com/p/leveldb/
%if 0%{?el7}%{?fedora}
VCS:		http://git.fedorahosted.org/git/leveldb.git
%endif
Source0:        http://leveldb.googlecode.com/files/%{name}-%{version}.tar.gz

Patch1:         leveldb-2.0.7-tests.patch

BuildRequires:  gcc-c++
BuildRequires:  snappy-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool


%description
LevelDB is a fast key-value storage library written at Google that provides an
ordered mapping from string keys to string values.

%package devel
Summary:        The development files for %{name}
Group:          Development/Libraries
Requires:       pkgconfig
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Additional header files for development with %{name}.

%prep
%setup -q
%if 0%{?__isa_bits} == 32
%patch1 -p1
%endif

%build
CFLAGS="%{optflags} -DNDEBUG" CXXFLAGS="%{optflags} -DNDEBUG" %configure --disable-static --with-pic || :
make %{?_smp_mflags}


%install
mkdir -p %{buildroot}%{_libdir} \
    %{buildroot}%{_includedir}/%{name}

rm -rf libleveldb.a
install -pm 755 libleveldb.so.1.9 %{buildroot}%{_libdir}/.
pushd %{buildroot}%{_libdir}
ln -s libleveldb.so.1.9 libleveldb.so.1
popd
install -pm 644 libleveldb.so %{buildroot}%{_libdir}/.
cp -a include/%{name}/* %{buildroot}%{_includedir}/%{name}/.

%check
%ifarch armv5tel armv7hl %{power64}
# FIXME a couple of tests are failing on these secondary arches, see
# https://bugzilla.redhat.com/908800
make check || true
%else
%if 0%{?__isa_bits} == 32
make check || true
%else
make check
%endif
# x86_64, ppc, ppc64, ppc64v7 s390, and s390x are fine
%endif

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc doc/ AUTHORS LICENSE README
%{_libdir}/lib%{name}.so.*


%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so


%changelog
* Wed Jul  8 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.0.7-1
- Upgrade to Basho's 2.0.7 (fork!)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Tomas Hozza <thozza@redhat.com> - 1.12.0-9
- rebuild with newer gcc to resolve linking issues with Ceph

* Sun Mar  1 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.0-8
- F-23: rebuild for gcc5 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 25 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.12.0-5
- Don't build with assertions

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.12.0-3
- Backported Basho's patch (see rhbz#982980)

* Mon Jul 01 2013 gil cattaneo <puntogil@libero.it> 1.12.0-2
- add SuspendCompactions and ResumeCompactions methods for allow leveldbjni build

* Sat Jun 29 2013 gil cattaneo <puntogil@libero.it> - 1.12.0-1
- update to 1.12.0

* Wed Feb 27 2013 gil cattaneo <puntogil@libero.it> - 1.9.0-1
- update to 1.9.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Feb 07 2013 Karsten Hopp <karsten@redhat.com> 1.7.0-5
- temporarily ignore result of self checks on PPC* (rhbz #908800)

* Thu Nov 29 2012 gil cattaneo <puntogil@libero.it> - 1.7.0-4
- Applied patch for allow leveldbjni build

* Sat Oct 27 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.7.0-3
- Dirty workarounds for failed tests on ARM

* Sat Oct 27 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.7.0-2
- Restored patch no.2

* Sat Oct 27 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.7.0-1
- Ver. 1.7.0 (API/ABI compatible bugfix release)

* Tue Aug 21 2012 Dan Horák <dan[at]danny.cz> - 1.5.0-4
- add workaround for big endians eg. s390(x)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.5.0-2
- Cleaned up spec by removing EL5-related stuff
- Added notes about the patches

* Fri Jun 15 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.5.0-1
- Ver. 1.5.0

* Thu May 17 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.4.0-1
- Initial package
