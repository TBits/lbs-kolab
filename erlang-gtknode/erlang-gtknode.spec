%global realname gtknode
%global upstream massemanet
%global git_tag 19ddfd5
%global patchnumber 0
%{?filter_setup:
%filter_provides_in %{_libdir}/erlang/lib/.*\.so$
%filter_setup
}


Name:		erlang-%{realname}
Version:	0.32
Release:	9.20110310git19ddfd5%{?dist}
Summary:	Erlang GTK2 binding
Group:		Development/Languages
License:	MIT
URL:		https://github.com/massemanet/gtknode
# wget --no-check-certificate --content-disposition https://github.com/massemanet/gtknode/tarball/19ddfd5
Source0:	%{upstream}-%{realname}-%{git_tag}.tar.gz
# The following patches were sent upstream - https://github.com/massemanet/gtknode/pull/2
Patch1:		erlang-gtknode-0001-Fix-OTP-R15B-compatibility-issue-re-run-instead-of-r.patch
Patch2:		erlang-gtknode-0002-Fix-for-R15B-usage-of-deprecated-http.patch
Patch3:		erlang-gtknode-0003-Off-by-one-error.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	erlang-erl_interface
BuildRequires:	erlang-rebar
BuildRequires:	gtk2-devel
BuildRequires:	libglade2-devel
BuildRequires:  python-devel
Requires:	erlang-erts
Requires:	erlang-kernel
Requires:	erlang-stdlib


%description
Erlang GTK2 binding.


%prep
%setup -q -n %{upstream}-%{realname}-%{git_tag}
%patch1 -p1
%patch2 -p1
%patch3 -p1


%build
autoreconf -ivf
%{configure}
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/doc/
rm -rf %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/examples/
rm -rf %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/src/
rm -rf %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/src/


%files
%doc AUTHORS COPYING README doc/announce
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv/bin/
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/bin/%{realname}


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-9.20110310git19ddfd5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-8.20110310git19ddfd5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-7.20110310git19ddfd5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Sep 01 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.32-6.20110310git19ddfd5
- Fixed FTBFS

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-5.20110310git19ddfd5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-4.20110310git19ddfd5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-3.20110310git19ddfd5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.32-2.20110310git19ddfd5
- Changed versioning scheme
- Added comment about tarball retrieving
- Fixed building with R15B

* Fri May 18 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.32-1
- Ver. 0.32
