%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname ebloom
%{?filter_setup:
%filter_provides_in %{_libdir}/erlang/lib/.*\.so$
%filter_setup
}
%{expand: %(NIF_VER=`rpm -q erlang-erts --provides | grep --color=no erl_nif_version` ; if [ "$NIF_VER" != "" ]; then echo %%global __erlang_nif_version $NIF_VER ; fi)}
%{expand: %(DRV_VER=`rpm -q erlang-erts --provides | grep --color=no erl_drv_version` ; if [ "$DRV_VER" != "" ]; then echo %%global __erlang_drv_version $DRV_VER ; fi)}


Name:		erlang-%{realname}
Version:	2.0.0
Release:	3%{?dist}
Summary:	A NIF wrapper around a basic bloom filter
Group:		Development/Languages
# c_src/bloom_filter.hpp and c_src/serialyzer.hpp are licensed under CPL
# and the rest of the sources are licensed under ASL 2.0
License:	ASL 2.0 and CPL
URL:		https://github.com/basho/ebloom
%if 0%{?rhel} > 6 || 0%{?fedora}
VCS:		scm:git:https://github.com/basho/ebloom.git
%endif
Source0:	https://github.com/basho/ebloom/archive/%{version}/%{realname}-%{version}.tar.gz
BuildRequires:	erlang-rebar
BuildRequires:	erlang-rpm-macros >= 0.1.4
BuildRequires:  gcc-c++
# erlang:load_nif/2
Requires:erlang-erts%{?_isa} >= R14B
Requires:erlang-kernel%{?_isa}
Requires:erlang-stdlib%{?_isa}
%{?__erlang_nif_version:Requires: %{__erlang_nif_version}}


%description
A NIF wrapper around a basic bloom filter.


%prep
%setup -q -n %{realname}-%{version}


%build
rebar compile -vv


%install
install -p -m 0644 -D ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -p -m 0644 -D ebin/%{realname}.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 0755 -D priv/%{realname}_nifs.so %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/%{realname}_nifs.so


%check
rebar eunit -v


%files
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv/
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/%{realname}_nifs.so


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.0.0-2
- Rebuilt for GCC 5 C++11 ABI change

* Tue Nov 04 2014 Peter Lemenkov <lemenkov@gmail.com> - 2.0.0-1
- Ver. 2.0.0 (just a version bump - no API/ABI changes)
- Rebuild with Erlang 17.3.3

* Thu Aug 28 2014 Peter Lemenkov <lemenkov@gmail.com> - 1.1.2-6
- Rebuild with Erlang 17.2.1

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.1.2-4
- Use new erlang macros to build with $RPM_OPT/LD_FLAGS etc, verbosely

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 10 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.1.2-1
- Ver. 1.1.2

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.1-1
- Ver. 1.1.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 22 2011 Peter Lemenkov <lemenkov@gmail.com> - 1.0.2-4
- Pass proper cxxflags to the C++ compiler (rhbz #669722) too

* Fri Jan 21 2011 Peter Lemenkov <lemenkov@gmail.com> - 1.0.2-3
- Pass proper cflags to the C compiler (rhbz #669722)

* Tue Jan 11 2011 Peter Lemenkov <lemenkov@gmail.com> - 1.0.2-2
- Filtered out NIF library from Provides

* Fri Nov 12 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.0.2-1
- Initial build

