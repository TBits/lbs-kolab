%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname bitcask
%global upstream basho
%global git_tag fa139ea
%global patchnumber 0
%{?filter_setup:
%filter_provides_in %{_libdir}/erlang/lib/.*\.so$
%filter_setup
}
%{expand: %(NIF_VER=`rpm -q erlang-erts --provides | grep --color=no erl_nif_version` ; if [ "$NIF_VER" != "" ]; then echo %%global __erlang_nif_version $NIF_VER ; fi)}
%{expand: %(DRV_VER=`rpm -q erlang-erts --provides | grep --color=no erl_drv_version` ; if [ "$DRV_VER" != "" ]; then echo %%global __erlang_drv_version $DRV_VER ; fi)}


Name:		erlang-%{realname}
Version:	2.0.1
Release:	1%{?dist}
Summary:	Eric Brewer-inspired key/value store
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/bitcask
%if 0%{?el7}%{?fedora}
VCS:		scm:git:https://github.com/basho/bitcask.git
%endif
# wget --content-disposition https://github.com/basho/bitcask/tarball/2.0.1
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz
Source1:	bitcask.licensing
BuildRequires:	erlang-cuttlefish
BuildRequires:	erlang-meck
BuildRequires:	erlang-rebar
BuildRequires:	erlang-rpm-macros >= 0.1.4
# Error:erlang(erlang:load_nif/2) in R12B and below
# Error:erlang(erlang:max/2) in R12B and below
# Error:erlang(erlang:nif_error/1) in R13B and below
# Error:erlang(os:timestamp/0) in R12B and below
Requires:	erlang-erts%{?_isa} >= R14B
Requires:	erlang-kernel%{?_isa}
# Error:erlang(queue:member/2) in R12B and below
Requires:	erlang-stdlib%{?_isa} >= R13B
%{?__erlang_nif_version:Requires: %{__erlang_nif_version}}


%description
Eric Brewer-inspired key/value store.


%prep
%setup -q -n %{upstream}-%{realname}-%{git_tag}


%build
rebar compile -vv


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,include,priv}
install -p -m 0644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -p -m 0644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 0644 include/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include
install -p -m 0755 priv/%{realname}.so %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/
install -p -m 0644 priv/*.schema %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/


%check
rebar eunit skip_deps=true -v || :


%files
%doc README.md THANKS doc/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/*.hrl
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/%{realname}.so
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/*.schema


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Nov 04 2014 Peter Lemenkov <lemenkov@gmail.com> - 1.6.3-6
- Rebuild with Erlang 17.3.3

* Thu Aug 28 2014 Peter Lemenkov <lemenkov@gmail.com> - 1.6.3-5
- Rebuild with Erlang 17.2.1

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.6.3-3
- Use new erlang macros to build with $RPM_OPT/LD_FLAGS etc, verbosely

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jul 31 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.6.3-1
- Ver. 1.6.3

* Sun Apr 07 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.6.1-1
- Ver. 1.6.1

* Sun Mar 10 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.6.0-1
- Ver. 1.6.0
- Fix FTBFS in Rawhide (F19)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 11 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.5.2-1
- Ver. 1.5.2 (Bugfix release)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.5.1-2
- Require specific %%{_isa} to avoid multiarch issues

* Thu May 17 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.5.1-1
- Ver. 1.5.1

* Fri Sep 16 2011 Peter Lemenkov <lemenkov@gmail.com> - 1.2.0-1
- Ver. 1.2.0

* Fri Jan 14 2011 Peter Lemenkov <lemenkov@gmail.com> - 1.1.5-1
- Ver. 1.1.5
- Pass optflags to C-compiler

* Fri Nov 12 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.1.4-1
- Initial build

