%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname webmachine
%global upstream basho
%global debug_package %{nil}
%global git_tag 7677c24
%global patchnumber 0


Name:		erlang-%{realname}
Version:	1.10.8
Release:	1%{?dist}
Summary:	A REST-based system for building web applications
Group:		Development/Languages
License:	ASL 2.0
URL:		http://webmachine.basho.com/
# wget --content-disposition https://github.com/basho/webmachine/tarball/1.10.8
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz
Patch1:     erlang-webmachine-1.10.8-relax-deps.patch
BuildRequires:	erlang-mochiweb >= 2.9.0
BuildRequires:	erlang-rebar

Requires:	erlang-crypto%{?_isa}
# Error:erlang(lists:keyfind/3) in R12B and below
Requires:	erlang-erts%{?_isa} >= R13B
Requires:	erlang-inets%{?_isa}
Requires:	erlang-kernel%{?_isa}
Requires:	erlang-mochiweb%{?_isa}
Requires:	erlang-ssl%{?_isa}
Requires:	erlang-stdlib%{?_isa} >= R12B-5


%description
A REST-based system for building web applications.


%prep
%setup -q -n %{upstream}-%{realname}-%{git_tag}
sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src
%patch1 -p1
chmod 644 src/wmtrace_resource.erl
chmod -x demo/start.sh
chmod -x priv/trace/wmtrace.css
chmod -x priv/trace/wmtrace.js

chmod +x priv/templates/start.sh

# Fix FTBFS with Erlang R16B
sed -i -e "/warnings_as_errors/d" rebar.config


%build
rebar compile -v
#make edoc
#rm -f docs/edoc-info


%install
install -D -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -m 644 ebin/%{realname}.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -m 644 ebin/%{realname}_*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -m 644 ebin/%{realname}_sup.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -m 644 ebin/wmtrace_resource.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -m 644 ebin/wrq.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -d %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include
install -m 644 include/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include
cp -r priv %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}
cp -r www %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}


%check
rebar eunit skip_deps=true -v || :


%files
%doc demo docs/http-headers-status-v3.png LICENSE README.org THANKS
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/www
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/*.hrl
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/*
%{_libdir}/erlang/lib/%{realname}-%{version}/www/*


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Sep 01 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.1-3
- Don't treat warnings as errors (fixes FTBFS with Erlang R16B)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Apr 07 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.1-1
- Ver. 1.10.1

* Fri Mar 22 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.0-1
- Ver. 1.10.0

* Sun Mar 03 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.9.3-1
- Ver. 1.9.3

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Aug 19 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.9.2-1
- Ver. 1.9.2
- Add _isa to the Requires
- Drop defattr directive

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 18 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.9.1-1
- Ver. 1.9.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Peter Lemenkov <lemenkov@gmail.com> - 1.8.0-2
- Cosmetic

* Mon Jan 10 2011 Peter Lemenkov <lemenkov@gmail.com> - 1.8.0-1
- Ver. 1.8.0

* Sat Oct 30 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.7.3-1
- Initial build

