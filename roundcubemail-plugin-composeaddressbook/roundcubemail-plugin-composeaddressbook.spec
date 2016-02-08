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

%global roundcube %{_datadir}/roundcubemail
%global roundcube_plugins %{roundcube}/plugins
%global roundcube_conf %{_sysconfdir}/roundcubemail
%global roundcube_log %{_var}/log/roundcubemail
%global roundcube_lib %{_var}/lib/roundcubemail

Name:       roundcubemail-plugin-composeaddressbook
Version:    5.0
Release:    0.1.beta3%{?dist}
Summary:    Show address book recipient selector during Compose

Group:      Applications/Internet
License:    AGPLv3+ and GPLv3+
URL:        http://www.kolab.org

Source0:    compose_addressbook-5.0b3.tgz

BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:  noarch

Requires:   roundcubemail >= 0.9

%description
Show an address book recipient selector for Roundcube Webmail

%prep
%setup -q -c

%build

%install
rm -rf %{buildroot}
mkdir -p \
    %{buildroot}%{roundcube_conf} \
    %{buildroot}%{roundcube_plugins}
cp -a compose_addressbook %{buildroot}%{roundcube_plugins}/

mv %{buildroot}%{roundcube_plugins}/compose_addressbook/config.inc.php.dist %{buildroot}%{roundcube_conf}/compose_addressbook.inc.php
pushd %{buildroot}%{roundcube_plugins}/compose_addressbook/
ln -s ../../../../..%{roundcube_conf}/compose_addressbook.inc.php config.inc.php
popd

%post
if [ -f "%{php_inidir}/apc.ini" -o -f "%{php_inidir}/apcu.ini" ]; then
    if [ ! -z "`grep ^apc.enabled=1 %{php_inidir}/apc{,u}.ini`" ]; then
%if 0%{?with_systemd}
        /bin/systemctl condrestart %{httpd_name}.service
%else
        /sbin/service %{httpd_name} condrestart
%endif
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{roundcube_conf}
%attr(0640,root,%{httpd_group}) %config(noreplace) %{roundcube_conf}/*.php
%dir %{roundcube}
%dir %{roundcube_plugins}
%{roundcube_plugins}/compose_addressbook

%changelog
* Tue Sep  3 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 5.0-0.1.beta3
- New package
