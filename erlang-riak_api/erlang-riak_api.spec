%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname riak_api
%global upstream basho
#
# This package contains only arch-independent data but install it into
# arch-dependent directory thus making this package arch-dependent. In order to
# suppress empty *-debuginfo generation we have to explicitly order
# debuginfo-generator to skip trying to build *-debuiginfo for that package.
#
%global debug_package %{nil}
%global git_tag 9883774
%global patchnumber 0


Name:		erlang-%{realname}
Version:	2.1.1
Release:	1%{?dist}
Summary:	Riak Client APIs
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/riak_api
%if 0%{?rhel} > 6 || 0%{?fedora}
VCS:		https://github.com/basho/riak_pb.git
%endif
# wget --content-disposition https://github.com/basho/riak_api/tarball/2.1.1
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz
Patch1:     erlang-riak_api-2.1.1-relax-deps.patch

BuildRequires:	erlang-lager >= 1.2.2
BuildRequires:	erlang-meck
BuildRequires:	erlang-os_mon
BuildRequires:	erlang-rebar
BuildRequires:	erlang-riak_core >= 2.1.1
BuildRequires:	erlang-riak_pb >= 1.3.0
Requires:	erlang-erts%{?_isa}
Requires:	erlang-folsom%{?_isa} >= 0.7.0
Requires:	erlang-kernel%{?_isa}
Requires:	erlang-lager%{?_isa} >= 1.2.2
Requires:	erlang-riak_core%{?_isa} >= 2.1.1
Requires:	erlang-riak_pb%{?_isa} >= 1.3.0
Requires:	erlang-stdlib%{?_isa}


%description
This OTP application encapsulates services for presenting Riak's public-facing
interfaces. Currently this means a generic interface for exposing Protocol
Buffers-based services; HTTP services via Webmachine will be moved here at a
later time.


%prep
%setup -q -n %{upstream}-%{realname}-b41b7a9
sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src
%patch1 -p1

%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,priv}
install -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 priv/* %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/.


%check
rebar eunit skip_deps=true -v || :


%files
%doc README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/*


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jul 31 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.2-2
- Fix version mismatch

* Wed Jul 31 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.2-1
- Ver. 1.3.2

* Sun Mar 24 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.1-2
- Added builddep on os_mon

* Sun Mar 24 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.1-1
- Ver. 1.3.1

* Mon Mar 11 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.0-1
- Ver. 1.3.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 12 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.1-1
- Ver. 1.2.1

* Wed Sep 05 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.0-1
- Initial build
