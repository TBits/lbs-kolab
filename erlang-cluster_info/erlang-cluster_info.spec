%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname cluster_info
%global upstream basho
%global debug_package %{nil}
%global git_tag e231144
%global patchnumber 0


Name:		erlang-%{realname}
Version:	2.0.2
Release:	1%{?dist}
Summary:	Cluster info/postmortem inspector for Erlang applications
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/cluster_info
# wget --content-disposition https://github.com/basho/cluster_info/tarball/2.0.2
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz
BuildRequires:	erlang-rebar
# erlang:get_stacktrace/0
Requires:	erlang-erts%{?_isa} >= R12B
Requires:	erlang-kernel%{?_isa}
Requires:	erlang-riak_err%{?_isa}
Requires:	erlang-sasl%{?_isa}
Requires:	erlang-stdlib%{?_isa}


%description
Cluster info/postmortem inspector for Erlang applications.


%prep
%setup -q -n %{upstream}-%{realname}-1d8bc2a
sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src


%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 ebin/%{realname}*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin


%check
rebar eunit -v


%files
%doc LICENSE README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}*.beam


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 10 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.2.3-1
- Ver. 1.2.3

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 12 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.2-1
- Ver. 1.2.2
- Switched upstream to Basho

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-0.5.20101229gitd077716
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-0.4.20101229gitd077716
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Feb 20 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.1.0-0.3.20101229gitd077716
- Changed Source0 again

* Sun Jan 30 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.1.0-0.2.20101229gitd077716
- Changed Source0 url

* Sat Jan 22 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.1.0-0.1.20101229gitd077716
- Initial build
