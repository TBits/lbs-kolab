%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname eper
%global upstream massemanet
%global debug_package %{nil}
%global patch_level 0
%global git_tag 69364c7


Name:		erlang-%{realname}
Version:	0.78
Release:	1%{?dist}
Summary:	Erlang performance and debugging tools
Group:		Development/Languages
License:	MIT
URL:		https://github.com/massemanet/eper
# wget --content-disposition https://github.com/massemanet/eper/tarball/0.78
Source0:	%{upstream}-%{realname}-%{version}-%{patch_level}-g%{git_tag}.tar.gz
BuildRequires:	erlang-rebar
Requires:	erlang-crypto
Requires:	erlang-erlsom
# Error:erlang(lists:keyfind/3) in R12B and below
Requires:	erlang-erts >= R13B
Requires:	erlang-getopt
Requires:	erlang-gtknode
Requires:	erlang-kernel
Requires:	erlang-runtime_tools
Requires:	erlang-stdlib


%description
This is a loose collection of Erlang Performance related tools:

 * sherk - a profiler, similar to Linux oprofile or MacOs shark
 * gperf - a graphical performance monitor; shows CPU, memory and network usage
 * dtop  - similar to unix top
 * redbug- similar to the OTP dbg application, but safer, better etc.


%prep
%setup -q -n %{upstream}-%{realname}-cbf1da6
rm -f src/getopt.erl


%build
rebar compile -v


%install
install -p -m 0644 -D ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -p -m 0644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -d %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/bin
install -p -m 0755 priv/bin/{dtop,gperf,ntop,redbug,sherk} %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/bin
install -d %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/glade
install -p -m 0644 src/*.glade %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/glade


%clean
rm -rf %{buildroot}


%files
%doc AUTHORS COPYING README doc/redbug.txt
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv/bin/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv/glade/
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/bin/*
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/glade/*.glade


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-8.20120621git16bae32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-7.20120621git16bae32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-6.20120621git16bae32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-5.20120621git16bae32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-4.20120621git16bae32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-3.20120621git16bae32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 03 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.60-2.20120621git16bae32
- Latest git tag
- Minor spec cleanups

* Fri Sep 16 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.60-1.20120501git592ef2
- Ver. 0.60.gitc592ef2
