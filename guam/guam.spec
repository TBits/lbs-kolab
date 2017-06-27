%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global debug_package %{nil}

%global realname kolab_guam

%global guam_user guam
%global guam_group guam

%if 0%{?suse_version} < 1 && 0%{?fedora} < 1 && 0%{?rhel} < 7
%global with_systemd 0
%else
%global with_systemd 1
%endif

%define lock_version() %{1}%{?_isa} = %(rpm -q --queryformat "%{VERSION}" %{1})

Name:               guam
Version:            0.9.2
Release:            2%{?dist}
Summary:            A Smart Reverse IMAP Proxy

Group:              System Environment/Daemons
License:            GPLv3+
URL:                https://kolab.org/about/guam

Source0:            https://mirror.kolabenterprise.com/pub/releases/guam-%{version}.tar.gz
Source100:          plesk.sys.config

Patch0001:          0001-Avoid-empty-lines-in-the-responses-to-IMAP-clients.patch
Patch0002:          guam-0.9.2-T25795.patch

Patch9991:          guam-0.9.1-relax-dependencies.patch
Patch9992:          guam-0.9.2-set-version-number.patch

BuildRequires:      erlang >= 17.4
BuildRequires:      erlang-asn1
BuildRequires:      erlang-common_test
BuildRequires:      erlang-compiler
BuildRequires:      erlang-crypto
BuildRequires:      erlang-debugger
BuildRequires:      erlang-eimap >= 0.2.4
BuildRequires:      erlang-erts
BuildRequires:      erlang-et
BuildRequires:      erlang-goldrush >= 0.1.8
BuildRequires:      erlang-kernel
BuildRequires:      erlang-lager >= 3.1.0
BuildRequires:      erlang-lager_syslog >= 2.0.3
BuildRequires:      erlang-mnesia
BuildRequires:      erlang-observer
BuildRequires:      erlang-public_key
BuildRequires:      erlang-rebar >= 2.5.1
BuildRequires:      erlang-runtime_tools
BuildRequires:      erlang-sasl
BuildRequires:      erlang-snmp
BuildRequires:      erlang-ssh
BuildRequires:      erlang-ssl
BuildRequires:      erlang-stdlib
BuildRequires:      erlang-syntax_tools
BuildRequires:      erlang-syslog >= 1.0.3
BuildRequires:      erlang-test_server
BuildRequires:      erlang-tools
BuildRequires:      erlang-webtool
BuildRequires:      erlang-wx
BuildRequires:      erlang-xmerl

Requires(pre):      shadow-utils
Requires(postun):   shadow-utils

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
Guam is a smart, unjustly outcasted Reverse IMAP Proxy that lives at
the perimeter of your IMAP environment.

%prep
%setup -q

%patch0001 -p1
%patch0002 -p1

%patch9991 -p1
%patch9992 -p1

%build
rebar compile
mkdir -p deps

pushd rel
ENABLE_STATIC=no rebar generate
popd

%install
mkdir -p \
    %{buildroot}/opt \
    %{buildroot}%{_sbindir} \
    %{buildroot}%{_sysconfdir}/guam/ \
%if 0%{?with_systemd}
    %{buildroot}%{_unitdir}/ \
%else
    %{buildroot}%{_initddir}/ \
%endif
    %{buildroot}%{_var}/log/

%if 0%{?with_systemd}
install -p -m 644 contrib/guam.service \
    %{buildroot}%{_unitdir}/guam.service
%else
install -p -m 755 contrib/guam.sysvinit \
    %{buildroot}%{_initddir}/guam
%endif

cp -a rel/%{realname} %{buildroot}/opt/.

cat > %{buildroot}%{_sbindir}/guam << EOF
#!/bin/bash
exec /opt/kolab_guam/bin/kolab_guam \$*
EOF

mv %{buildroot}/opt/%{realname}/releases/*/sys.config \
    %{buildroot}%{_sysconfdir}/guam/sys.config

%if 0%{?plesk}
install -m 644 -p %{SOURCE100} %{buildroot}%{_sysconfdir}/guam/sys.config
%endif

ln -s ../../../..%{_sysconfdir}/%{name}/sys.config \
    $(ls -1d %{buildroot}/opt/%{realname}/releases/*/)/sys.config

mv %{buildroot}/opt/%{realname}/log %{buildroot}%{_var}/log/guam
ln -s ../..%{_var}/log/guam %{buildroot}/opt/%{realname}/log

pushd %{buildroot}/opt/%{realname}/lib
for dir in $(ls -d */ | grep -v kolab_guam); do
    dir=$(basename ${dir})
    if [ ! -d %{_libdir}/erlang/lib/${dir} ]; then
        echo "Skipping deletion of ${dir}, no equivalent in %{_libdir}/erlang/lib/"
    else
        rm -rvf ${dir}
        ln -sv ../../..%{_libdir}/erlang/lib/${dir} ${dir}
    fi
done
popd

%check
rebar skip_deps=true eunit -v

%pre
if [ $1 == 1 ]; then
    /usr/sbin/groupadd --system %{guam_group} 2> /dev/null || :
    /usr/sbin/useradd -c "Guam Service" -d /opt/kolab_guam -g %{guam_group} \
        -s /sbin/nologin --system %{guam_user} 2> /dev/null || :
fi

%postun
%if 0%{?with_systemd}
%systemd_postun
%endif
if [ $1 == 0 ]; then
    /usr/sbin/userdel %{guam_user} 2>/dev/null || :
    /usr/sbin/groupdel %{guam_group} 2>/dev/null || :
fi

%if 0%{?with_systemd}
%post
%systemd_post guam.service

if [ ! -f "/etc/guam/dh_2048.pem" ]; then
    openssl gendh -out /etc/guam/dh_2048.pem -2 2048 >/dev/null 2>&1
fi

%preun
%systemd_preun guam.service

%posttrans
test -f /etc/sysconfig/guam-disable-posttrans || \
    systemctl try-restart guam.service 2>&1 || :

%else
%post
chkconfig --add guam >/dev/null 2>&1 || :

if [ ! -f "/etc/guam/dh_2048.pem" ]; then
    openssl gendh -out /etc/guam/dh_2048.pem -2 2048 >/dev/null 2>&1
fi

%posttrans
test -f /etc/sysconfig/guam-disable-posttrans || \
    %{_sbindir}/service restart guam 2>&1 || :
%endif

%files
%attr(0750,root,root) %{_sbindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/sys.config
%attr(0640,%{guam_user},%{guam_group}) %{_var}/log/%{name}/

%if 0%{?with_systemd}
%{_unitdir}/%{name}.service
%else
%{_initddir}/%{name}
%endif

/opt/%{realname}/

%changelog
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
