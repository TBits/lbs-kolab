%global realname gettext
%global debug_package %{nil}
%global git_tag b55cb72


Name:		erlang-%{realname}
Version:	2.1.0
Release:	0.10.20101022git%{git_tag}%{?dist}
Summary:	Erlang internationalization library
Group:		Development/Languages
License:	MIT
URL:		http://github.com/etnt/gettext
# wget http://github.com/etnt/gettext/tarball/b55cb72
Source0:	etnt-%{realname}-%{git_tag}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	erlang-erts
Requires:	erlang-erts >= R12B-5
Requires:	erlang-kernel >= R12B-5
Requires:	erlang-stdlib >= R12B-5
Requires:	erlang-sasl >= R12B-5


%description
Erlang internationalization library.


%prep
%setup -q -n etnt-%{realname}-%{git_tag}


%build
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include
install -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 include/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/*.hrl


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-0.10.20101022gitb55cb72
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-0.9.20101022gitb55cb72
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-0.8.20101022gitb55cb72
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-0.7.20101022gitb55cb72
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-0.6.20101022gitb55cb72
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-0.5.20101022gitb55cb72
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-0.4.20101022gitb55cb72
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-0.3.20101022gitb55cb72
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 28 2010 Peter Lemenkov <lemenkov@gmail.com> - 2.1.0-0.2.20101022gitb55cb72
- Ensure consistency in macro usage

* Fri Oct 22 2010 Peter Lemenkov <lemenkov@gmail.com> - 2.1.0-0.1.20101022gitb55cb72
- Initial build

