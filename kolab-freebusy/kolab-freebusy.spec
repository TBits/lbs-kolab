#!BuildIgnore: lighttpd
#!BuildIgnore: thttpd
#!BuildIgnore: nginx
%{!?php_inidir: %global php_inidir %{_sysconfdir}/php.d}

%if 0%{?suse_version} < 1 && 0%{?fedora} < 1 && 0%{?rhel} < 7
%global with_systemd 0
%else
%global with_systemd 1
%endif

%if 0%{?suse_version}
%global httpd_group www
%global httpd_name apache2
%global httpd_user wwwrun
%else
%global httpd_group apache
%global httpd_name httpd
%global httpd_user apache
%endif

%global _ap_sysconfdir %{_sysconfdir}/%{httpd_name}

Name:           kolab-freebusy
Version:        1.0.7
Release:        2%{?dist}
Summary:        Kolab Free/Busy Web Presentation Layer

Group:          Applications/Internet
License:        AGPLv3+
URL:            http://kolab.org/about/kolab-freebusy
Source0:        http://mirror.kolabsys.com/pub/releases/%{name}-%{version}+dep.tar.gz
Source1:        kolab-freebusy.logrotate

Patch0001:      0001-Consider-recurrence-exceptions-when-computing-busy-t.patch

BuildArch:      noarch

%if 0%{?suse_version}
BuildRequires:  roundcubemail
BuildRequires:  roundcubemail-plugins-kolab
Requires:       http_daemon
Requires:       php
%else
Requires:       webserver
Requires:       php-common >= 5.3
%endif

Requires:       kolab-utils
Requires:       logrotate
Requires:       php-ldap
Requires:       php-pear(Net_LDAP3)
Requires:       roundcubemail
Requires:       roundcubemail-plugins-kolab

%description
This software enables a multi-sourced publication of Free/Busy information
for its users.

%prep
%setup -q

%patch0001 -p1

%build

%install
mkdir -p \
    %{buildroot}/%{_ap_sysconfdir}/conf.d/ \
    %{buildroot}/%{_sysconfdir}/%{name}/ \
    %{buildroot}/%{_datadir}/%{name}/config \
    %{buildroot}/%{_localstatedir}/cache/%{name}/ \
    %{buildroot}/%{_localstatedir}/log/%{name}/

mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
cp -pr %SOURCE1 %{buildroot}%{_sysconfdir}/logrotate.d/kolab-freebusy

cat > %{buildroot}/%{_ap_sysconfdir}/conf.d/%{name}.conf <<EOF
ScriptAlias /freebusy /usr/share/kolab-freebusy/public_html/index.php
EOF

cp -a lib %{buildroot}/%{_datadir}/%{name}/lib

rm -rf %{buildroot}/%{_datadir}/%{name}/lib/plugins
rm -rf %{buildroot}/%{_datadir}/%{name}/lib/Roundcube
pushd %{buildroot}/%{_datadir}/%{name}/lib/
ln -s ../../roundcubemail/plugins/ plugins
ln -s ../../roundcubemail/program/lib/Roundcube/ Roundcube
popd

cp -a public_html %{buildroot}/%{_datadir}/%{name}/public_html
cp -a vendor %{buildroot}/%{_datadir}/%{name}/vendor

cp -a config/config.ini.sample %{buildroot}/%{_sysconfdir}/%{name}/config.ini

pushd %{buildroot}/%{_datadir}/%{name}/config
ln -s ../../../..%{_sysconfdir}/%{name}/config.ini config.ini
ln -s ../../../..%{_sysconfdir}/roundcubemail/config.inc.php config.inc.php
ln -s ../../../..%{_sysconfdir}/roundcubemail/defaults.inc.php defaults.inc.php
popd

pushd %{buildroot}/%{_datadir}/%{name}/
ln -s ../../..%{_localstatedir}/log/%{name} logs
popd

find %{buildroot}/%{_datadir}/%{name} -type f -name ".*" -delete

%pre
# This is replaced by an actual directory
if [ -L "%{_datadir}/kolab-freebusy/config" ]; then
    rm -rf "%{_datadir}/kolab-freebusy/config"
fi

%post
if [ -f "%{php_inidir}/apc.ini" ]; then
    if [ ! -z "`grep ^apc.enabled=1 %{php_inidir}/apc.ini`" ]; then
%if 0%{?with_systemd}
        /bin/systemctl condrestart %{httpd_name}.service
%else
        /sbin/service %{httpd_name} condrestart
%endif
    fi
fi

%files
%defattr(-,root,root,-)
%doc README.md
%if 0%{?suse_version}
%dir %{_ap_sysconfdir}
%dir %{_ap_sysconfdir}/conf.d
%endif
%config(noreplace) %{_ap_sysconfdir}/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0750,root,%{httpd_group}) %dir %{_sysconfdir}/%{name}/
%attr(0640,root,%{httpd_group}) %config(noreplace) %{_sysconfdir}/%{name}/config.ini
%{_datadir}/%{name}/
%attr(0770,root,%{httpd_group}) %{_localstatedir}/cache/%{name}
%attr(0770,root,%{httpd_group}) %{_localstatedir}/log/%{name}

%changelog
* Sun Feb 22 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.0.7-2
- Correctly render Free/Busy for recurring events with exceptions (#4665)

* Sun Feb 15 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.0.7-1
- Release of version 1.0.7

* Fri Jan 23 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.0.6-1
- Release 1.0.6

* Wed Aug 20 2014 Daniel Hoffend <dh@dotlan.net> - 1.0.5-2
- added fix for loading Net_LDAP3

* Thu Aug 14 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.0.5-1
- Release version 1.0.5

* Wed May 21 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.0.4-1
- New upstream version, enabling real-time Free/Busy directly
  from IMAP data.

* Tue Nov 26 2013 Daniel Hoffend <dh@dotlan.net> - 1.0.2-5
- Added logrotate script

* Fri Nov 15 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.0.2-4
- Depend on kolab-utils

* Tue Oct 29 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.0.2-3
- Do not require PHP itself

* Tue Apr 30 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.0.2-2
- Ship fix for lower-casing attributes (#1777)

* Thu Feb 21 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.0.2-1
- Repack of original sources

* Mon Feb 18 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.0-1
- First package
