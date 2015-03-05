Name:           xapian-core
Version:        1.2.16
Release:        1%{?dist}
Summary:        The Xapian Probabilistic Information Retrieval Library

Group:          Applications/Databases
License:        GPLv2+
URL:            http://www.xapian.org/
# Repack for the sake of Debian packaging in the OBS
Source0:        http://www.oligarchy.co.uk/xapian/%{version}/%{name}-%{version}.tar.gz

Patch1:         xapian-add-snippet-generator.patch
Patch2:         xapian-fix-snippet-first-char-nonword.patch
Patch3:         xapian-some-cjk-chars-are-punctuation.patch
Patch4:         xapian-change-snippet-generator-to-deque.patch
Patch5:         xapian-fix-snippet-generator-CJK.patch
Patch6:         xapian-fix-snippet-generator-punctuation-in-match.patch
Patch9:         xapian-autoconf-2.63.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  libuuid-devel
BuildRequires:  zlib-devel

%if 0%{?suse_version}
Requires:       libxapian22 = %{version}
%else
Requires:       %{name}-libs = %{version}-%{release}
%endif

%description
Xapian is an Open Source Probabilistic Information Retrieval Library. It
offers a highly adaptable toolkit that allows developers to easily add advanced
indexing and search facilities to applications

%if 0%{?suse_version}
%package -n libxapian22
%else
%package libs
%endif
Summary:        Xapian search engine libraries
Group:          System Environment/Libraries
%if 0%{?suse_version} > 1220 && 0%{?suse_version}
Requires:       libz1
%endif

%if 0%{?suse_version}
%description -n libxapian22
%else
%description libs
%endif
Xapian is an Open Source Probabilistic Information Retrieval framework. It
offers a highly adaptable toolkit that allows developers to easily add advanced
indexing and search facilities to applications. This package provides the
libraries for applications using Xapian functionality

%package devel
Group:          Development/Libraries
Summary:        Files needed for building packages which use Xapian
Requires:       %{name} = %{version}-%{release}
%if 0%{?suse_version}
Requires:       libxapian22 = %{version}
%else
Requires:       %{name}-libs = %{version}-%{release}
%endif
Requires:       libuuid-devel

%description devel
Xapian is an Open Source Probabilistic Information Retrieval framework. It
offers a highly adaptable toolkit that allows developers to easily add advanced
indexing and search facilities to applications. This package provides the
files needed for building packages which use Xapian

%prep
%setup -q

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%if 0%{?rhel} < 7 && 0%{?fedora} < 1 && 0%{?suse_version} < 1
%patch9 -p1
%endif

%build
aclocal -I m4
automake --add-missing
autoreconf -v
# Disable SSE on x86, but leave it intact for x86_64
%ifarch x86_64
%configure --disable-static
%else
%configure --disable-static --disable-sse
%endif

# Remove rpath as per https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

# Remove libtool archives
# find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Remove the dev docs, we pick them up below
rm -rf %{buildroot}%{_datadir}/doc/%{name}

%if 0%{?suse_version}
%post -n libxapian22 -p /sbin/ldconfig
%else
%post libs -p /sbin/ldconfig
%endif

%if 0%{?suse_version}
%postun -n libxapian22 -p /sbin/ldconfig
%else
%postun libs -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root,-)
%{_bindir}/xapian*
%exclude %{_bindir}/xapian-config
%{_bindir}/quest
%{_bindir}/delve
%{_bindir}/copydatabase
%{_bindir}/simpleindex
%{_bindir}/simplesearch
%{_bindir}/simpleexpand
# man pages may be gzipped, hence the trailing wildcard.
%{_mandir}/man1/xapian*
%exclude %{_mandir}/man1/xapian-config.1.gz
%{_mandir}/man1/quest.1*
%{_mandir}/man1/delve.1*
%{_mandir}/man1/copydatabase.1*

%if 0%{?suse_version}
%files -n libxapian22
%else
%files libs
%endif
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/libxapian.so.*

%files devel
%defattr(-,root,root,-)
%doc HACKING PLATFORMS docs/*html docs/apidoc docs/*pdf
%{_bindir}/xapian-config
%dir %{_includedir}/xapian
%{_includedir}/xapian.h
%{_includedir}/xapian/base.h
%{_includedir}/xapian/compactor.h
%{_includedir}/xapian/database.h
%{_includedir}/xapian/dbfactory.h
%{_includedir}/xapian/deprecated.h
%{_includedir}/xapian/derefwrapper.h
%{_includedir}/xapian/document.h
%{_includedir}/xapian/enquire.h
%{_includedir}/xapian/error.h
%{_includedir}/xapian/errorhandler.h
%{_includedir}/xapian/expanddecider.h
%{_includedir}/xapian/keymaker.h
%{_includedir}/xapian/matchspy.h
%{_includedir}/xapian/positioniterator.h
%{_includedir}/xapian/postingiterator.h
%{_includedir}/xapian/postingsource.h
%{_includedir}/xapian/query.h
%{_includedir}/xapian/queryparser.h
%{_includedir}/xapian/registry.h
%{_includedir}/xapian/stem.h
%{_includedir}/xapian/snippetgenerator.h
%{_includedir}/xapian/termgenerator.h
%{_includedir}/xapian/termiterator.h
%{_includedir}/xapian/types.h
%{_includedir}/xapian/unicode.h
%{_includedir}/xapian/valueiterator.h
%{_includedir}/xapian/valuesetmatchdecider.h
%{_includedir}/xapian/version.h
%{_includedir}/xapian/visibility.h
%{_includedir}/xapian/weight.h
%{_libdir}/libxapian.so
%{_libdir}/libxapian.la
%if 0%{?suse_version}
%dir %{_libdir}/cmake
%endif
%{_libdir}/cmake/xapian
%{_datadir}/aclocal/xapian.m4
# man pages may be gzipped, hence the trailing wildcard.
%{_mandir}/man1/xapian-config.1*

%changelog
* Sun Jan 12 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.16-1
- Update to 1.2.16

* Fri Aug 23 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.15-1
- Update to 1.2.15

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 23 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.14
- Update to 1.2.14

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.12-1
- Update to 1.2.12

* Sun Apr 29 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.9-1
- Update to 1.2.9

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-2
- Rebuilt for c++ ABI breakage

* Sat Jan 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.8-1
- Update to 1.2.8

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 18 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.7-1
- Update to 1.2.7

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.4-1
- Update to 1.2.4

* Mon Aug 30 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3

* Thu Aug  5 2010 Adel Gadllah <adel.gadllah@gmail.com> - 1.2.2-5
- Reenable SSE on x86_64

* Thu Aug  5 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.2-4
- Disable SSE instructions by default

* Wed Jul 14 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.2-3
- And remove non spec cut-n-paste issue

* Wed Jul 14 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.2-2
- Add cmake stuff

* Wed Jul 14 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2

* Fri May  7 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.0-4
- Move license to libs package, a few other spc cleanups

* Fri May  7 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.0-3
- Add the libtool archive (temporarily) to fix build of bindings

* Sat May  1 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.0-2
- Upload new source 

* Sat May  1 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0
