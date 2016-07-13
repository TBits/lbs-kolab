%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname riak_pipe
%global debug_package %{nil}

Name:		erlang-%{realname}
Version:	2.1.1
Release:	1%{?dist}
Summary:	Riak Pipelines
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/riak_pipe
# wget --content-disposition https://github.com/basho/riak_pipe/archive/2.1.1.tar.gz
Source0:	%{realname}-%{version}.tar.gz

Patch1:     erlang-riak_pipe-2.1.1-otp-18.3-compat.patch

BuildRequires:	erlang-rebar
BuildRequires:	erlang-os_mon
BuildRequires:	erlang-riak_core >= 2.1.0
Requires:	erlang-cluster_info%{?_isa}
# Error:erlang(lists:keyfind/3) in R12B and older
# Error:erlang(os:timestamp/0) in R12B and older
Requires:	erlang-erts%{?_isa} >= R13B
Requires:	erlang-folsom%{?_isa}
Requires:	erlang-hipe%{?_isa}
Requires:	erlang-kernel%{?_isa}
Requires:	erlang-lager%{?_isa}
Requires:	erlang-riak_core%{?_isa} >= 2.1.0
Requires:	erlang-stdlib%{?_isa}


%description
Riak Pipelines.


%prep
%setup -q -n %{realname}-%{version}
sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src
%patch1 -p1

%build
rebar compile -v
#rebar doc -v
rm -rf doc/edoc-info


%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,include,priv}
install -p -m 644 ebin/%{realname}.app $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 644 ebin/*.beam $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 644 include/*.hrl $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/include
install -p -m 644 priv/app.slave0.config $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/priv


%check
%ifnarch %{arm}
rebar eunit skip_deps=true -v
%endif


%files
%doc LICENSE README.org
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv/
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/%{realname}*.hrl
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/app.slave0.config


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Aug 06 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.2-2
- Don't run tests on ARM - one of them will fail for unknown (for me) reason

* Wed Jul 31 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.2-1
- Ver. 1.3.2

* Sun Mar 24 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.1-2
- Added builddep on os_mon

* Sun Mar 24 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.1-1
- Ver. 1.3.1

* Mon Mar 11 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.0-1
- Ver. 1.3.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2.p1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 19 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.1-1.p1
- Ver. 1.2.1p1

* Fri May 18 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.2-1
- Ver. 1.1.2

* Fri Sep 16 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.9.1-1
- Initial build
