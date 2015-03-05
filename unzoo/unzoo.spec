Name:           unzoo
Version:        4.4
Release:        10%{?dist}
Summary:        ZOO archive extractor

Group:          Applications/Archiving
License:        Public Domain
URL:            http://archives.math.utk.edu/software/multi-platform/gap/util/unzoo.c
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        http://archives.math.utk.edu/software/multi-platform/gap/util/unzoo.c

%description
'unzoo' is a zoo archive extractor.  A zoo archive is a file that
contains several files, called its members, usually in compressed form
to save space.  'unzoo' can list all or selected members or extract
all or selected members, i.e., uncompress them and write them to
files.  It cannot add new members or delete members.  For this you
need the zoo archiver, called 'zoo', written by Rahul Dhesi.


%prep
%setup -Tc -n %{name}-%{version}
cp -a %{SOURCE0} .
cat %{SOURCE0} | sed -e '/SYNTAX/,/\*\//!d' | cut -c5- > unzoo.txt


%build
gcc %{optflags} -o unzoo -DSYS_IS_UNIX unzoo.c


%install
rm -rf %{buildroot}

# Install binaries
install -Dpm 755 unzoo %{buildroot}%{_bindir}/unzoo


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/unzoo
%doc unzoo.txt


%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar 26 2009 John W. Linville <linville@redhat.com> - 4.4-4
- Copy source to build directory so it is included in debuginfo

* Thu Mar 26 2009 John W. Linville <linville@redhat.com> - 4.4-3
- Use setup macro in prep phase (cleaner spec, generates debuginfo)
- Add release info in changelog

* Wed Mar 25 2009 John W. Linville <linville@redhat.com> - 4.4-2
- Revise in accordance with new package review comments

* Mon Mar 23 2009 John W. Linville <linville@redhat.com> - 4.4-1
- Initial release for Fedora
