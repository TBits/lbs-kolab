# Needed for opensuse build system
%if 0%{?opensuse_bs}
#!BuildIgnore:  boa
#!BuildIgnore:  cherokee
#!BuildIgnore:  nginx
#!BuildIgnore:  httpd-itk
#!BuildIgnore:  lighttpd
#!BuildIgnore:  thttpd

#!BuildIgnore:  php-mysqlnd
%endif

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

Name:           chwala
Version:        0.3.0
Release:        1%{?dist}
Summary:        Glorified WebDAV, done right

Group:          Applications/Internet
License:        AGPLv3+
URL:            http://chwala.org
Source0:        http://mirror.kolabsys.com/pub/releases/chwala-%{version}.tar.gz
Source2:        chwala.logrotate

Patch1:         chwala-0.2-suhosin.session.encrypt-php_flag.patch
Patch2:         0002-Use-folder-state-check-and-set-type-when-using-kolab.patch

BuildArch:      noarch

Requires:       php-pear(HTTP_Request2)
Requires:       php-Smarty >= 3.1.7
Requires:       roundcubemail
Requires:       roundcubemail-plugins-kolab
%if 0%{?suse_version}
Requires:       http_daemon
%else
Requires:       webserver
%endif

%if 0%{?suse_version}
BuildRequires:  roundcubemail
BuildRequires:  roundcubemail-plugins-kolab
%endif

%description
Chwala is the implementation of a modular, scalable, driver-backed file-
and media-storage, that with using an API, provides generated UI components
based on context and content, for the purpose of integration with 3rd
party applications.

%prep
%setup -q

%patch1 -p1
%patch2 -p1

%build

%install
mkdir -p \
    %{buildroot}/%{_ap_sysconfdir}/conf.d \
    %{buildroot}/%{_datadir}/%{name} \
    %{buildroot}/%{_localstatedir}/cache/%{name} \
    %{buildroot}/%{_localstatedir}/lib/%{name} \
    %{buildroot}/%{_localstatedir}/log/%{name}

install -pm 644 doc/chwala.conf %{buildroot}/%{_ap_sysconfdir}/conf.d/chwala.conf

mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
cp -pr %SOURCE2 %{buildroot}%{_sysconfdir}/logrotate.d/chwala

cp -a lib public_html %{buildroot}/usr/share/%{name}

pushd %{buildroot}/%{_datadir}/%{name}

pushd lib/ext
rm -rf Auth
rm -rf HTTP
rm -rf Mail
rm -rf Net
rm -rf PEAR*.php
rm -rf Roundcube
ln -s ../../../roundcubemail/program/lib/Roundcube Roundcube
popd

pushd lib/drivers/kolab/plugins
rm -rf kolab_auth libkolab
ln -s ../../../../../roundcubemail/plugins/kolab_auth kolab_auth
ln -s ../../../../../roundcubemail/plugins/libkolab libkolab
popd

ln -s ../../..%{_localstatedir}/cache/%{name} cache
ln -s ../../..%{_sysconfdir}/roundcubemail config
ln -s ../../..%{_localstatedir}/lib/%{name} temp
ln -s ../../..%{_localstatedir}/log/%{name} logs
popd

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
%doc README.md LICENSE
%{_ap_sysconfdir}/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_datadir}/%{name}
%attr(0750,%{httpd_user},%{httpd_group}) %{_localstatedir}/cache/%{name}
%attr(0750,%{httpd_user},%{httpd_group}) %{_localstatedir}/lib/%{name}
%attr(0750,%{httpd_user},%{httpd_group}) %{_localstatedir}/log/%{name}

%changelog
* Sat Feb 14 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3.0-2
- Use filder state check when accessing file folder (#4478)

* Sun Jan 11 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3.0-1
- Release of version 0.3.0

* Thu Feb 25 2014 Daniel Hoffend <dh@dotlan.net> - 0.2-4
- applied fix for recent libkolab changes

* Thu Jan 23 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.2-3
- Correct any suhosin.session.encrypt setting using .htaccess
- Correct source of chwala.conf

* Tue Nov 26 2013 Daniel Hoffend <dh@dotlan.net> - 0.2-1.1
- added logrotate script

* Sun Nov 24 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.2-1
- New upstream version

* Tue Oct 29 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.1-0.5
- Require only "webserver" or "http_daemon"

* Fri Aug  9 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.1-0.4
- New snapshot

* Tue May  7 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.1-0.2
- A first version of chwala
