%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname mochiweb
%global upstream mochi
%global debug_package %{nil}
%global git_tag 66a6535
%global patchnumber 0


Name:		erlang-%{realname}
Version:	2.9.2
Release:	1%{?dist}
Summary:	An Erlang library for building lightweight HTTP servers
Group:		Development/Libraries
License:	MIT
URL:		http://github.com/mochi/mochiweb
# wget --content-disposition https://github.com/mochi/mochiweb/tarball/v2.4.2
Source0:	%{upstream}-%{realname}-v%{version}-%{patchnumber}-g%{git_tag}.tar.gz
BuildRequires:	erlang-rebar
BuildRequires:	erlang-xmerl
Requires:	erlang-compiler%{?_isa}
Requires:	erlang-crypto%{?_isa}
# Error:erlang(binary:match/2) in R13B ale earlier
Requires:	erlang-erts%{?_isa} >= R14B
Requires:	erlang-inets%{?_isa}
Requires:	erlang-kernel%{?_isa}
Requires:	erlang-ssl%{?_isa}
# Error:erlang(unicode:characters_to_binary/1) in R12B and earlier
Requires:	erlang-stdlib%{?_isa} >= R13B
Requires:	erlang-syntax_tools%{?_isa}
Requires:	erlang-xmerl%{?_isa}
Provides:	%{realname} = %{version}-%{release}


%description
An Erlang library for building lightweight HTTP servers.


%prep
%setup -q -n %{upstream}-%{realname}-%{git_tag}


%build
rebar compile -v


%install
# base binary modules
install -D -m 644 ebin/%{realname}.app $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -m 644 ebin/*.beam $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/

# skeleton files
cp -arv scripts $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}
cp -arv support $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}


%check
rebar eunit -v


%files
%doc CHANGES.md LICENSE README examples
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochifmt.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochifmt_records.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochifmt_std.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiglobal.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochihex.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochijson.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochijson2.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochilists.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochilogfile2.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochinum.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochitemp.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiutf8.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_acceptor.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_base64url.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_charref.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_cookies.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_cover.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_echo.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_headers.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_html.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_http.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_io.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_mime.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_multipart.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_request.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_response.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_session.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_socket.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_socket_server.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_util.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_websocket.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/reloader.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/scripts
%{_libdir}/erlang/lib/%{realname}-%{version}/support


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Peter Lemenkov <lemenkov@gmail.com> - 2.4.2-2
- Fixed issue with R16B01

* Sat Mar 02 2013 Peter Lemenkov <lemenkov@gmail.com> - 2.4.2-1
- Ver. 2.4.2

* Thu Jan 31 2013 Peter Lemenkov <lemenkov@gmail.com> - 2.4.1-1
- Ver. 2.4.1

* Sat Jan 26 2013 Peter Lemenkov <lemenkov@gmail.com> - 2.4.0-2
- Fixed regression (see https://github.com/mochi/mochiweb/issues/97 )

* Fri Jan 25 2013 Peter Lemenkov <lemenkov@gmail.com> - 2.4.0-1
- Ver. 2.4.0 (fix for Erlang R16)
- Dropped patches for EL5 (Erlang R12B)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Apr 06 2011 Peter Lemenkov <lemenkov@gmail.com> - 1.4.1-5
- Don't remove test-file (rhbz #675699)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 22 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.4.1-3
- Added erlang-xmerl as BuildRequires

* Mon Nov 22 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.4.1-2
- Added accidentally removed dependency required for %%check

* Sat Nov 13 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.4.1-1
- Ver. 1.4.1

* Wed Oct 13 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.4.0-1
- Ver. 1.4.0

* Wed Sep 29 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.3-0.8.20100929git9687b40
- Narrowed BuildRequires
- Restricted explicit requirement for obsoleted fd_server module (rhbz #601152)
- Dropped upstreamed patch6

* Tue Aug 17 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.3-0.7.20100724git9a53dbd7
- Fix improper int to string conversion

* Wed Aug 11 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.3-0.6.20100724git9a53dbd7
- Fixed all tests on EL-5
- New git snapshot

* Tue Jul 13 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.3-0.5.20100507svn159
- Fixed several tests on EL-5 (enough to allow CouchDB to pass its own self-tests)

* Mon Jul 12 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.3-0.4.20100507svn159
- Rebuild with new Erlang
- Simplified spec-file

* Mon Jun  7 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.3-0.3.20100507svn159
- Added %%check target and fixed mochiweb:test()
- Fix EL-5 build

* Mon Jun  7 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.3-0.2.20100507svn159
- Removed accidentally added macro

* Mon May 31 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.3-0.1.20100507svn159
- New pre-release version (from VCS).

* Thu May 13 2010 Peter Lemenkov <lemenkov@gmail.com> - 0-0.1.svn154
- Initial package
