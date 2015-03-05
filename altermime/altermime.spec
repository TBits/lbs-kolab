Name:           altermime
Version:        0.3.10
Release:        9%{?dist}
Summary:        Alter MIME-encoded mailpacks

Group:          Applications/Internet
License:        BSD
URL:            http://www.pldaniels.com/altermime/
Source0:        http://www.pldaniels.com/altermime/altermime-%{version}.tar.gz
Patch0:         altermime-0.3.10-fprintf-compiler-error.patch
Patch1:         altermime-0.3.10-cflags.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
alterMIME is a small program which is used to alter MIME-encoded mailpacks.

alterMIME can:

 * Insert disclaimers
 * Insert arbitary X-headers
 * Modify existing headers
 * Remove attachments based on filename or content-type
 * Replace attachments based on filename 

%prep
%setup -q
%patch0 -p0
%patch1 -p0


%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ;
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
# Makefile has hardcoded paths
%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -m 755 altermime %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/*

%doc CHANGELOG LICENCE README


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Feb 11 2011 Tim Jackson <rpm@timj.co.uk> 0.3.10-5
- Ensure distribution-supplied CFLAGS are used during compile
- Fix build on F15

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 22 2008 Tim Jackson <rpm@timj.co.uk> 0.3.10-1
- Update to version 0.3.10

* Sat Jul 19 2008 Tim Jackson <rpm@timj.co.uk> 0.3.8-1
- Update to version 0.3.8

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.3.7-3
- Autorebuild for GCC 4.3

* Sat Sep 09 2006 Tim Jackson <rpm@timj.co.uk> 0.3.7-2
- Rebuild for FE6

* Fri Mar 31 2006 Tim Jackson <rpm@timj.co.uk> 0.3.7-1
- Update to 0.3.7

* Fri Feb 17 2006 Tim Jackson <rpm@timj.co.uk> 0.3.6-2
- Rebuild for FC5

* Wed Jan 11 2006 Tim Jackson <rpm@timj.co.uk> 0.3.6-1
- Intial build for FE
