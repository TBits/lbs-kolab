%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname riak_dt
%global upstream basho
%global debug_package %{nil}
%global git_tag f7981d4
%global patchnumber 0


Name:		erlang-%{realname}
Version:	2.1.0
Release:	1%{?dist}
Summary:	A set of state based CRDTs implemented in Erlang
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/riak_dt
# wget --content-disposition https://github.com/basho/riak_dt/tarball/2.1.0
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz

# Compile-time requirements
BuildRequires:	erlang-rebar

Requires:	erlang-kernel%{?_isa}
Requires:	erlang-stdlib%{?_isa} >= R13B

%description
A set of state based CRDTs implemented in Erlang.


%prep
%setup -q -n %{upstream}-%{realname}-6ab4a87
sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src

%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,include,priv}
install -p -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 644 include/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include


%check
rebar eunit skip_deps=true -v || :


%files
%doc LICENSE README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/*.hrl


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jul 02 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.2-1
- Ver. 1.3.2

* Sun Mar 24 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.1-2
- Fix webmachine dep

* Sun Mar 24 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.1-1
- Ver. 1.3.1

* Mon Mar 11 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.0-1
- Ver. 1.3.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-4.p1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Oct 20 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.1-3.p1
- Ver. 1.2.1p1

* Fri Oct 19 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.1-2
- Rebuild with new lager

* Wed Oct 10 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.1-1
- Ver. 1.2.1

* Wed Sep 05 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.0-1
- Ver. 1.2.0

* Thu Jul 19 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.2-3
- Re-export one handy function

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 18 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.2-1
- Ver. 1.1.2

* Fri Feb 25 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.14.1-1
- Ver. 0.14.1

* Sat Jan 22 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.14.0-1
- Ver. 0.14.0
- Dropped upstreamed patch

* Fri Nov 12 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.13.0-1
- Initial build

