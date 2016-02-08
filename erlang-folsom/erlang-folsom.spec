%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname folsom
%global upstream boundary
%global debug_package %{nil}
%global git_tag 38e2cce
%global patchnumber 0


Name:		erlang-%{realname}
Version:	0.8.2
Release:	1%{?dist}
Summary:	Erlang-based metrics system
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/boundary/folsom
# wget --content-disposition https://github.com/boundary/folsom/tarball/0.7.4
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz
# PowerPC-specific, backported from upstream
Patch1:		erlang-folsom-0001-Fix-for-PowerPC.patch
# Fedora/EPEL-specific
Patch3:		erlang-folsom-0003-Fix-for-Erlang-R14B-EPEL6.patch
BuildRequires:	erlang-bear
BuildRequires:	erlang-meck
BuildRequires:	erlang-rebar
Requires:	erlang-bear%{?_isa}
Requires:	erlang-erts%{?_isa}
Requires:	erlang-kernel%{?_isa}


%description
Folsom is an Erlang based metrics system inspired by Coda Hale's metrics.
The metrics API's purpose is to collect realtime metrics from your Erlang
applications and publish them via Erlang APIs and output plugins. Folsom is not
a persistent store. There are 6 types of metrics: counters, gauges, histograms
and timers, histories, meter_readers and meters. Metrics can be created, read
and updated via the folsom_metrics module.


%prep
%setup -q -n %{upstream}-%{realname}-%{git_tag}
%ifarch ppc %{power64}
%patch1 -p1 -b .ppc
%endif

sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src

%build
rebar compile -v


%install
install -D -m 644 ebin/%{realname}.app $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -m 644 ebin/%{realname}.beam $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -m 644 ebin/%{realname}_*.beam $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -D -m 644 include/%{realname}.hrl $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/include/%{realname}.hrl


%check
rebar eunit skip_deps=true -vv || :


%files
%doc LICENSE README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/%{realname}.hrl


%changelog
* Wed Jul  8 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.8.2-1
- Check in version 0.8.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 03 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.7.4-1
- Ver. 0.7.4

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 09 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.7.3-2
- Fix for Erlang R14B (EPEL6)

* Fri Dec 21 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.7.3-1
- Ver. 0.7.3

* Sun Sep 02 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.7.1-1
- Initial build
