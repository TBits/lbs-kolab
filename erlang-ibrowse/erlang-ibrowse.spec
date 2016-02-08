%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname ibrowse
%global debug_package %{nil}


Name:		erlang-%{realname}
Version:	4.0.2
Release:	1%{?dist}
Summary:	Erlang HTTP client
Group:		Development/Languages
License:	BSD or LGPLv2+
URL:		http://github.com/cmullaparthi/ibrowse
%if 0%{?rhel} > 6 || 0%{?fedora}
VCS:		scm:git:https://github.com/cmullaparthi/ibrowse.git
%endif
Source0:	https://github.com/cmullaparthi/ibrowse/archive/v%{version}/%{realname}-%{version}.tar.gz
# CouchDB-specific patch
Patch1:		erlang-ibrowse-0001-Support-SOCKS5-protocol-for-replication.patch
BuildRequires:	erlang-rebar
BuildRequires:	sed
Requires:	erlang-erts
Requires:	erlang-kernel
Requires:	erlang-ssl
Requires:	erlang-stdlib


%description
%{summary}.


%prep
%setup -q -n %{realname}-%{version}

# Use system-wide rebar
sed -i -e "s,./rebar,rebar,g" Makefile

%patch1 -p1 -b .socks5


%build
CFLAGS="%{optflags}" REBAR_FLAGS="--verbose 2" make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT%{_libdir}/erlang
rm -f $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_test.beam
sed -i -e "s,\,ibrowse_test,,g" $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -p -m 0644 -D include/ibrowse.hrl $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/include/ibrowse.hrl


%check
make test


%files
%doc BSD_LICENSE LICENSE
%doc CHANGELOG CONTRIBUTORS README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_app.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_http_client.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_lb.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_lib.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_socks5.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_sup.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/%{realname}.hrl


%changelog
* Thu Jul  9 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 4.0.2-1
- Check in version 4.0.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 23 2014 Peter Lemenkov <lemenkov@gmail.com> - 4.0.1-1
- Ver. 4.0.1
- Support only Fedora 18+, EL6+
- Added patch for CouchDB 1.6.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 02 2011 Peter Lemenkov <lemenkov@gmail.com> - 2.2.0-4
- Removed mentioning about test file from *.app

* Tue Jul 12 2011 Peter Lemenkov <lemenkov@gmail.com> - 2.2.0-3
- Fix building on EL-5

* Sun May 15 2011 Peter Lemenkov <lemenkov@gmail.com> - 2.2.0-2
- Added missing build requirements

* Sun May 15 2011 Peter Lemenkov <lemenkov@gmail.com> - 2.2.0-1
- Ver. 2.2.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Peter Lemenkov <lemenkov@gmail.com> - 2.1.3-1
- Ver. 2.1.3

* Wed Nov 10 2010 Peter Lemenkov <lemenkov@gmail.com> - 2.1.0-1
- Ver. 2.1.0

* Tue Sep 28 2010 Peter Lemenkov <lemenkov@gmail.com> - 2.0.1-1
- Ver. 2.0.1
- Narrowed BuildRequires

* Sun Jul 11 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.6.0-0.4.20100601git07153bc
- Add missing runtime requirement - erlang-sasl
- Rebuild with Erlang/OTP R14A

* Tue Jun  8 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.6.0-0.3.20100601git07153bc
- Also install header file

* Tue Jun  1 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.6.0-0.2.20100601git07153bc
- New git snapshot (with clarified licensing terms)

* Thu May 27 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.6.0-0.1.gita114ed3b
- Ver 1.6.0 from git with one patch ahead.

* Thu May 13 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.5.6-2
- Narrowed explicit requires

* Wed Apr  7 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.5.6-1
- initial package

