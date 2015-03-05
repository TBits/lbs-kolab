%if 0%{?suse_version}
Name:           libjansson4
%else
Name:		    jansson
%endif
Version:	    2.4
Release:	    2%{?dist}
Summary:	    C library for encoding, decoding and manipulating JSON data

Group:		    System Environment/Libraries
License:	    MIT
URL:		    http://www.digip.org/jansson/
Source0:	    http://www.digip.org/jansson/releases/jansson-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-sphinx

%description
Small library for parsing and writing JSON documents.

%package devel
Summary:        Header files for jansson
Group:          Development/Libraries
Requires:       %{name} = %{version}
Requires:       pkgconfig
Provides:       pkgconfig(jansson)

%description devel
Header files for developing applications making use of jansson.

%prep
%setup -q -n jansson-%{version}

%build
%configure --disable-static
make %{?_smp_mflags}
make html

%check
make check

%install
rm -rf "$RPM_BUILD_ROOT"
make install INSTALL="install -p" DESTDIR="$RPM_BUILD_ROOT"
rm "$RPM_BUILD_ROOT%{_libdir}"/*.la

%clean
rm -rf "$RPM_BUILD_ROOT"

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE CHANGES
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/_build/html/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/jansson.pc
%{_includedir}/*

%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 08 2012 Jiri Pirko <jpirko@redhat.com> 2.4-1
- Update to Jansson 2.4.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Jiri Pirko <jpirko@redhat.com> 2.3-1
- Update to Jansson 2.3.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 11 2011 Sean Middleditch <sean@middleditch.us> 2.1-1
- Update to Jansson 2.1.
- Drop Sphinx patch, no longer necessary.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 03 2010 Sean Middleditch <sean@middleditch.us> 1.3-1
- Update to Jansson 1.3.
- Disable warnings-as-errors for Sphinx documentation.

* Thu Jan 21 2010 Sean Middleditch <sean@middleditch.us> 1.2-1
- Update to Jansson 1.2.

* Thu Jan 11 2010 Sean Middleditch <sean@middleditch.us> 1.1.3-4
- Update jansson description per upstream's suggestions.
- Removed README from docs.

* Thu Jan 09 2010 Sean Middleditch <sean@middleditch.us> 1.1.3-3
- Correct misspelling of jansson in the pkg-config file.

* Thu Jan 09 2010 Sean Middleditch <sean@middleditch.us> 1.1.3-2
- Fix Changelog dates.
- Mix autoheader warning.
- Added make check.
- Build and install HTML documentation in -devel package.

* Thu Jan 07 2010 Sean Middleditch <sean@middleditch.us> 1.1.3-1
- Initial packaging for Fedora.
