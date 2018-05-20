%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global debug_package %{nil}

%global realname kolab_guam
%global binname guam

%if 0%{?suse_version} < 1 && 0%{?fedora} < 1 && 0%{?rhel} < 7
%global with_systemd 0
%else
%global with_systemd 1
%endif

%{!?_unitdir: %global _unitdir /usr/lib/systemd/system}

%define lock_version() %{1}%{?_isa} = %(rpm -q --queryformat "%%{VERSION}" %{1})

Name:               guam
Version:            0.9.4
Release:            7%{?dist}
Summary:            A Smart Reverse IMAP Proxy

Group:              System Environment/Daemons
License:            GPLv3+
URL:                https://kolab.org/about/guam

Source0:            https://mirror.kolabenterprise.com/pub/releases/guam-%{version}.tar.gz
Source100:          plesk.sys.config

Patch9991:          make-it-very-easy-on-rebar3.patch
Patch9992:          guam-priv-no-delete.patch
Patch9993:          guam-0.9.2-stalling-client-buffer-and-split-command-handling.patch

BuildRequires:      erlang >= 17.4
BuildRequires:      erlang-asn1
BuildRequires:      erlang-common_test
BuildRequires:      erlang-compiler
BuildRequires:      erlang-crypto
BuildRequires:      erlang-debugger
BuildRequires:      erlang-eimap >= 0.3.0
BuildRequires:      erlang-erts
BuildRequires:      erlang-et
BuildRequires:      erlang-goldrush >= 0.1.8
BuildRequires:      erlang-kernel
BuildRequires:      erlang-lager >= 3.1.0
BuildRequires:      erlang-lager_syslog >= 2.0.3
BuildRequires:      erlang-mnesia
BuildRequires:      erlang-observer
BuildRequires:      erlang-public_key
BuildRequires:      erlang-rebar3 >= 3.3.2
BuildRequires:      erlang-rpm-macros
BuildRequires:      erlang-runtime_tools
BuildRequires:      erlang-sasl
BuildRequires:      erlang-snmp
BuildRequires:      erlang-ssh
BuildRequires:      erlang-ssl
BuildRequires:      erlang-stdlib
BuildRequires:      erlang-syntax_tools
BuildRequires:      erlang-syslog >= 1.0.3
BuildRequires:      erlang-tools
BuildRequires:      erlang-wx
BuildRequires:      erlang-xmerl

Requires:           %lock_version erlang
Requires:           %lock_version erlang-eimap
Requires:           %lock_version erlang-goldrush
Requires:           %lock_version erlang-lager
Requires:           %lock_version erlang-lager_syslog

%if 0%{?with_systemd}
%if 0%{?suse_version}
Requires(post):     systemd
Requires(postun):   systemd
Requires(preun):    systemd
%else
Requires(post):     systemd-units
Requires(postun):   systemd-units
Requires(preun):    coreutils
Requires(preun):    systemd-units
%endif
%else
Requires(post):     chkconfig
Requires(post):     initscripts
Requires(postun):   initscripts
Requires(preun):    chkconfig
Requires(preun):    initscripts
%endif

%description
Guam is a smart, unjustly outcast Reverse IMAP Proxy that lives at
the perimeter of your IMAP environment.

%prep
%setup -q

%patch9991 -p1
%patch9992 -p1
%patch9993 -p1

sed -i 's/"0\.9\.0"/"%{version}"/' rebar.config

%build

DEBUG=1
export DEBUG

HEX_OFFLINE=true
export HEX_OFFLINE

rebar3 release \
    --dev-mode false \
    --relname %{name} \
    --relvsn %{version} \
    --verbose

%install

find -type f | sort

mkdir -p \
    %{buildroot}%{_sysconfdir}/%{name}/ \
    %{buildroot}%{_sbindir} \
    %{buildroot}%{_erldir}/bin/ \
    %{buildroot}%{_erllibdir}/%{realname}-%{version}/ \
%if 0%{?with_systemd}
    %{buildroot}%{_unitdir}/ \
%else
    %{buildroot}%{_initddir}/ \
%endif
    %{buildroot}%{_var}/log/%{name}/

# Configuration
cp _build/default/rel/%{name}/etc/sys.config \
    %{buildroot}%{_sysconfdir}/%{name}/sys.config
cp _build/default/rel/%{name}/vm.args \
    %{buildroot}%{_sysconfdir}/%{name}/vm.args

# Service scripts
%if 0%{?with_systemd}
install -p -m 644 contrib/%{name}.service \
    %{buildroot}%{_unitdir}/%{name}.service
%else
install -p -m 755 contrib/%{name}.sysvinit \
    %{buildroot}%{_initddir}/%{name}
%endif

pushd %{buildroot}%{_erldir}/bin/
ln -s ../lib/%{realname}-%{version}/bin/%{binname} %{realname}
popd

cp -a _build/default/rel/%{name}/bin %{buildroot}%{_erllibdir}/%{realname}-%{version}/
cp -a _build/default/rel/%{name}/lib/%{realname}-%{version}/ebin/ %{buildroot}%{_erllibdir}/%{realname}-%{version}/
cp -a _build/default/rel/%{name}/releases/ %{buildroot}%{_erllibdir}/%{realname}-%{version}/

%if 0%{?plesk}
install -m 644 -p %{SOURCE100} %{buildroot}%{_sysconfdir}/guam/sys.config
%endif

pushd %{buildroot}%{_erllibdir}/%{realname}-%{version}/releases/%{version}/
rm sys.config vm.args
ln -sv ../../../../../../..%{_sysconfdir}/%{name}/sys.config sys.config
ln -sv ../../../../../../..%{_sysconfdir}/%{name}/vm.args vm.args
popd

pushd %{buildroot}%{_erllibdir}/%{realname}-%{version}/
ln -s ../../lib lib
ln -s ../../../../..%{_var}/log/%{name} log
popd

cat > %{buildroot}%{_sbindir}/%{name} << EOF
#!/bin/bash
exec %{_erllibdir}/%{realname}-%{version}/bin/%{binname} \$*
EOF

%check
# Hopeless on -0.9
rebar3 eunit -v || :

%postun
%if 0%{?with_systemd}
%systemd_postun
%endif

%if 0%{?with_systemd}
%post
%systemd_post %{name}.service

if [ ! -f "/etc/guam/dh_2048.pem" ]; then
    openssl gendh -out /etc/guam/dh_2048.pem -2 2048 >/dev/null 2>&1 || \
    openssl dhparam -out /etc/guam/dh_2048.pem -2 2048 >/dev/null 2>&1
fi

%preun
%systemd_preun %{name}.service

%posttrans
test -f /etc/sysconfig/guam-disable-posttrans || \
    systemctl try-restart %{name}.service 2>&1 || :

%else
%post
chkconfig --add %{name} >/dev/null 2>&1 || :

if [ ! -f "/etc/guam/dh_2048.pem" ]; then
    openssl gendh -out /etc/guam/dh_2048.pem -2 2048 >/dev/null 2>&1 || \
    openssl dhparam -out /etc/guam/dh_2048.pem -2 2048 >/dev/null 2>&1
fi

%posttrans
test -f /etc/sysconfig/guam-disable-posttrans || \
    %{_sbindir}/service restart %{name} 2>&1 || :
%endif

%files
%config(noreplace) %{_sysconfdir}/%{name}/sys.config
%config(noreplace) %{_sysconfdir}/%{name}/vm.args
%attr(0750,root,root) %{_sbindir}/%{name}
%{_libdir}/erlang/bin/%{realname}
%{_libdir}/erlang/lib/%{realname}-%{version}
%attr(0640,root,root) %{_var}/log/%{name}/

%if 0%{?with_systemd}
%{_unitdir}/%{name}.service
%else
%{_initddir}/%{name}
%endif

%changelog
* Sat May 19 2018 Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com> - 0.9.4-7
- Fix generating dh params file on more recent openssl versions

* Tue May 08 2018 Christoph Erhardt <kolab@sicherha.de> - 0.9.4-6
- Apply patch that fixes stalling client buffers and handling of split commands

* Fri May 04 2018 Christoph Erhardt <kolab@sicherha.de> - 0.9.4-5
- Make logs go to /var/log/guam

* Sat Apr 21 2018 Christoph Erhardt <kolab@sicherha.de> - 0.9.4-4
- Fix packaging, dependencies and more stuff

* Thu Apr 19 2018 Christoph Erhardt <kolab@sicherha.de> - 0.9.4-3
- Use script rather than symlink

* Thu Apr 19 2018 Christoph Erhardt <kolab@sicherha.de> - 0.9.4-2
- Ship correct variants of sys.config and vm.args

* Sun Apr 15 2018 Christoph Erhardt <kolab@sicherha.de> - 0.9.4-1
- Release version 0.9.4

* Tue Feb 27 2018 Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com> - 0.9.2-3
- Allow empty lines in commands

* Mon Jun 26 2017 Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com> - 0.9.2-2
- Fix T25795

* Mon Jun 19 2017 Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com> - 0.9.2-1
- Release version 0.9.2

* Tue Jul 12 2016 Aaron Seigo <seigo@kolabsystems.com> - 0.8.3-1
- Release of version 0.8.3

* Fri Jul  8 2016 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.8.2-2
- Fix T1345

* Wed Jul  6 2016 Aaron Seigo <seigo@kolabsystems.com> - 0.8.2-1
- Release of version 0.8.2

* Tue Jul  5 2016 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.8.1-1
- Release of version 0.8.1

* Fri Jun 10 2016 Aaron Seigo <seigo@kolabsystems.com>
- Package version 0.8

* Tue Feb  2 2016 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.7.1-1
- Check in systemd init script fixes

* Mon Jan  4 2016 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.7.0-1
- Release of 0.7.0

* Mon Dec 21 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.6-0.1.git
- Check in 0.6 from git master HEAD to introduce CI/CD

* Wed Dec 16 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.5-0.1.git
- Release of 0.5
- Enhance groupware filtering

* Tue Dec  8 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.4-0.1.git
- Release of 0.4

* Mon Dec  7 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3-0.1.git
- Third iteration with more/better TLS configuration support

* Mon Nov 30 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.2-0.1.git
- Second iteration with TLS configuration

* Thu Nov 26 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.1-0.1.git
- First package
