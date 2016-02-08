%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname eleveldb
%global upstream basho
%global git_tag b51dce2
%global patchnumber 0
%{?filter_setup:
%filter_provides_in %{_libdir}/erlang/lib/.*\.so$
%filter_setup
}
%{expand: %(NIF_VER=`rpm -q erlang-erts --provides | grep --color=no erl_nif_version` ; if [ "$NIF_VER" != "" ]; then echo %%global __erlang_nif_version $NIF_VER ; fi)}
%{expand: %(DRV_VER=`rpm -q erlang-erts --provides | grep --color=no erl_drv_version` ; if [ "$DRV_VER" != "" ]; then echo %%global __erlang_drv_version $DRV_VER ; fi)}


Name:		erlang-%{realname}
Version:	2.1.2
Release:	1%{?dist}
Summary:	Erlang LevelDB API
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/eleveldb
%if 0%{?el7}%{?fedora}
VCS:		scm:git:https://github.com/basho/eleveldb.git
%endif
# wget --content-disposition https://github.com/basho/eleveldb/tarball/2.1.2
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz

Patch1:     erlang-eleveldb-2.1.2-system-libraries.patch
Patch2:     erlang-eleveldb-2.1.2-set-version.patch

BuildRequires:  erlang-cuttlefish >= 2.0.1
BuildRequires:	erlang-rebar
BuildRequires:	erlang-rpm-macros >= 0.1.4
BuildRequires:  gcc-c++
BuildRequires:	leveldb-devel >= 2.0.7
BuildRequires:	snappy-devel
# Error:erlang(erlang:load_nif/2) in R12B and older
# Error:erlang(erlang:nif_error/1) in R13B and older
# Error:erlang(lists:keyfind/3) in R12B and older
Requires:	erlang-erts%{?_isa} >= R14B
Requires:	erlang-kernel%{?_isa}
Requires:	erlang-stdlib%{?_isa}
%{?__erlang_nif_version:Requires: %{__erlang_nif_version}}


%description
Erlang LevelDB API.


%prep
%setup -q -n %{upstream}-%{realname}-5bdcab1
rm -f c_src/build_deps.sh
rm -f c_src/snappy-1.0.4.tar.gz
%patch1 -p1
%patch2 -p1

%if 0%{?fc17}%{?fc18}%{?fc20}%{?fc21}%{?fc22}
# Another one FIXME
rm -rf test/cacheleak.erl
%endif


%build
rebar compile -vv


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,priv}
install -p -m 0644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -p -m 0644 ebin/%{realname}.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 0644 ebin/%{realname}_bump.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 0755 priv/%{realname}.so %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/
install -p -m 0644 priv/*.schema %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/


%check
rebar eunit -v || :


%files
%doc README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv/
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_bump.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/%{realname}.so
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/*.schema



%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Nov 04 2014 Peter Lemenkov <lemenkov@gmail.com> - 1.3.2-7
- Rebuild with Erlang 17.3.3

* Thu Aug 28 2014 Peter Lemenkov <lemenkov@gmail.com> - 1.3.2-6
- Rebuild with Erlang 17.2.1

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.3.2-4
- Use new erlang macros to build with $RPM_OPT/LD_FLAGS etc, verbosely
- Disable cache leak test on F-20, F-21, and F-22 (#1107767, #1106223)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 03 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.2-1
- Ver. 1.3.2

* Tue Apr 02 2013 Dan Horák <dan[at]danny.cz> - 1.3.0-2
- fix build on s390

* Mon Mar 11 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.0-1
- Ver. 1.3.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 11 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.2-1
- Ver. 1.2.2

* Wed Jul 18 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.0-2
- Remove EL5-specific stuff from spec-file
- Enable tests

* Thu May 17 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.0-1
- Ver. 1.1.0

* Fri Sep 16 2011 Peter Lemenkov <lemenkov@gmail.com> - 1.0.0-1
- Ver. 1.0.0
