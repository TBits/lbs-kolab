Name:           perl-Convert-TNEF
Version:        0.18
Release:        2%{?dist}
Summary:        Perl module to read TNEF files
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Convert-TNEF/
Source0:        http://www.cpan.org/authors/id/D/DO/DOUGW/Convert-TNEF-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(integer)
BuildRequires:  perl(IO::Wrap)
BuildRequires:  perl(MIME::Body) >= 4.109
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
TNEF stands for Transport Neutral Encapsulation Format, and if you've
ever been unfortunate enough to receive one of these files as an email
attachment, you may want to use this module.

%prep
%setup -q -n Convert-TNEF-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc Changes README
%{perl_vendorlib}/Convert/
%{_mandir}/man3/Convert::TNEF.3pm*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct  2 2013 Paul Howarth <paul@city-fan.org> - 0.18-1
- Update to 0.18
  - Add IO::Wrap dependency to Makefile.PL (CPAN RT#78412)
  - Change longname() to detect names in newer versions of Outlook
    (CPAN RT#78484)
- Specify all dependencies
- Drop %%defattr, redundant since rpm 4.4
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Don't need to remove empty directories from the buildroot
- Don't use macros for commands

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 29 2013 Petr Pisar <ppisar@redhat.com> - 0.17-21
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 23 2012 Petr Pisar <ppisar@redhat.com> - 0.17-18
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.17-16
- Perl mass rebuild

* Wed Feb  9 2011 Paul Howarth <paul@city-fan.org> - 0.17-15
- BR: perl(IO::Wrap) as perl(MIME::Body) no longer pulls it in

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.17-13
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.17-12
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.17-11
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.17-8
- Rebuild for new perl

* Tue Apr 17 2007 Steven Pritchard <steve@kspei.com> 0.17-7
- Use fixperms macro instead of our own chmod incantation.
- Reformat to more closely match cpanspec output.
- BR MIME::Body instead of perl-MIME-tools.
- BR ExtUtils::MakeMaker.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 0.17-6
- Fix find option order.

* Mon Sep 05 2005 Steven Pritchard <steve@kspei.com> 0.17-5
- Spec cleanup (closer to FE perl spec template).
- Include COPYING and Artistic.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Apr 26 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.17-0.fdr.3
- Specfile rewrite according to current fedora.us perl spec template.
- Fix License.
- BuildRequires perl-MIME-tools (bug 370).

* Fri Jul 11 2003 Dams <anvil[AT]livna.org> 0:0.17-0.fdr.2
- Changed Group tag value
- Added "make test" in build section
- Added missing directory

* Sun Jun 15 2003 Dams <anvil[AT]livna.org>
- Initial build.
