%if 0%{?opensuse_bs}
#!BuildIgnore:  systemd
%endif

%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%if 0%{?suse_version} || 0%{?fedora} > 17 || 0%{?rhel} > 6
%global with_systemd 1
%{!?_unitdir:   %global _unitdir /usr/lib/systemd/system/}
%else
%global with_systemd 0
%endif

%global bonnie_user bonnie
%global bonnie_user_id 415
%global bonnie_group bonnie
%global bonnie_group_id 415

Name:               bonnie
Version:            0.3.5
Release:            1%{?dist}
Summary:            Bonnie for Kolab Groupware

Group:              Applications/System
License:            GPLv3+
URL:                https://kolab.org
Source0:            %{name}-%{version}.tar.gz

BuildArch:          noarch

Requires(pre):      /usr/sbin/useradd
Requires(pre):      /usr/sbin/usermod
Requires(pre):      /usr/sbin/groupadd

%if 0%{?with_systemd}
%if 0%{?suse_version}
Requires(post):     systemd
Requires(postun):   systemd
Requires(preun):    systemd
%else
%if 0%{?opensuse_bs} == 0
Requires(post):     systemd-units
Requires(postun):   systemd-units
Requires(preun):    coreutils
Requires(preun):    systemd-units
%endif
%endif
%else
Requires(post):     chkconfig
Requires(post):     initscripts
Requires(postun):   initscripts
Requires(preun):    chkconfig
Requires(preun):    initscripts
%endif

%description
Bonnie for Kolab Groupware

%package elasticsearch
Summary:            Elasticsearch meta-package for Bonnie
Group:              Applications/System
Provides:           %{name}(output) = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:           %{name}(storage) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:           python-elasticsearch >= 1.0.0

%description elasticsearch
This meta-package pulls in the Elasticsearch output and storage channels
for Bonnie workers.

%package riak
Summary:            Riak meta-package for Bonnie
Group:              Applications/System
Provides:           %{name}(output) = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:           %{name}(storage) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:           python-riak >= 2.1.0

%description riak
This meta-package pulls in the Riak output and storage channels
for Bonnie workers.

%package broker
Summary:            The Bonnie broker
Group:              Applications/System
Requires(pre):      %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:           python-sqlalchemy >= 0.8.0
Requires:           python-tornado
Requires:           python-zmq

%description broker
Bonnie for Kolab Groupware

%package collector
Summary:            The Bonnie collector
Group:              Applications/System
Requires(pre):      %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires(pre):      cyrus-imapd
Requires:           python-zmq

%description collector
Bonnie for Kolab Groupware

%package dealer
Summary:            The Bonnie dealer
Group:              Applications/System
Requires(pre):      %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires(pre):      cyrus-imapd
Requires:           python-tornado
Requires:           python-zmq

%description dealer
Bonnie for Kolab Groupware

%package worker
Summary:            The Bonnie worker
Group:              Applications/System
Requires:           %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:           %{name}(output) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:           %{name}(storage) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:           python-zmq

%description worker
Bonnie for Kolab Groupware

%package wui
Summary:            The Bonnie Web UI
Group:              Applications/System
Requires:           bonnie-flask
Requires:           python-flask
Requires:           python-flask-bootstrap
Requires:           python-flask-httpauth
Requires:           python-flask-login
Requires:           python-flask-script
Requires:           python-flask-sqlalchemy

%description wui
Bonnie for Kolab Groupware

%prep
%setup -q

%build

%install
mkdir -p \
    %{buildroot}/%{_sysconfdir}/%{name} \
    %{buildroot}/%{_bindir} \
    %{buildroot}/%{_sbindir} \
    %{buildroot}/%{python_sitelib} \
    %{buildroot}/%{_var}/lib/%{name} \
    %{buildroot}/%{_var}/log/%{name}

%{__install} -m640 -p conf/bonnie.conf %{buildroot}/%{_sysconfdir}/%{name}

%{__install} -m755 -p broker.py %{buildroot}/%{_sbindir}/bonnie-broker
%{__install} -m755 -p collector.py %{buildroot}/%{_sbindir}/bonnie-collector
%{__install} -m755 -p dealer-async.py %{buildroot}/%{_bindir}/bonnie-dealer
%{__install} -m755 -p dealer-sync.py %{buildroot}/%{_bindir}/bonnie-dealer-sync
%{__install} -m755 -p worker.py %{buildroot}/%{_sbindir}/bonnie-worker

%{__cp} -a bonnie %{buildroot}/%{python_sitelib}

%if 0%{?with_systemd}
mkdir -p %{buildroot}/%{_unitdir}
%{__install} -p -m 644 contrib/bonnie-broker.systemd %{buildroot}/%{_unitdir}/bonnie-broker.service
%{__install} -p -m 644 contrib/bonnie-collector.systemd %{buildroot}/%{_unitdir}/bonnie-collector.service
%{__install} -p -m 644 contrib/bonnie-worker.systemd %{buildroot}/%{_unitdir}/bonnie-worker.service
mkdir -p %{buildroot}/%{_prefix}/lib/tmpfiles.d/
%{__install} -p -m 644 contrib/bonnie.tmpfiles.d.conf %{buildroot}/%{_prefix}/lib/tmpfiles.d/bonnie.conf
mkdir -p %{buildroot}/run
%{__install} -d -m 755 %{buildroot}/run/bonnie
%else
mkdir -p %{buildroot}/%{_initddir}
%{__install} -p -m 755 contrib/bonnie-broker.sysvinit %{buildroot}/%{_initrddir}/bonnie-broker
%{__install} -p -m 755 contrib/bonnie-collector.sysvinit %{buildroot}/%{_initrddir}/bonnie-collector
%{__install} -p -m 755 contrib/bonnie-worker.sysvinit %{buildroot}/%{_initrddir}/bonnie-worker
%endif

%if 0%{?suse_version}
mkdir -p %{buildroot}/%{_var}/adm/fillup-templates/
%{__install} -p -m 644 contrib/bonnie-broker.sysconfig %{buildroot}/%{_var}/adm/fillup-templates/sysconfig.bonnie-broker
%{__install} -p -m 644 contrib/bonnie-collector.sysconfig %{buildroot}/%{_var}/adm/fillup-templates/sysconfig.bonnie-collector
%{__install} -p -m 644 contrib/bonnie-worker.sysconfig %{buildroot}/%{_var}/adm/fillup-templates/sysconfig.bonnie-worker
%else
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
%{__install} -p -m 644 contrib/bonnie-broker.sysconfig %{buildroot}/%{_sysconfdir}/sysconfig/bonnie-broker
%{__install} -p -m 644 contrib/bonnie-collector.sysconfig %{buildroot}/%{_sysconfdir}/sysconfig/bonnie-collector
%{__install} -p -m 644 contrib/bonnie-worker.sysconfig %{buildroot}/%{_sysconfdir}/sysconfig/bonnie-worker
%endif

%pre
# Add the kolab user and group accounts
getent group %{bonnie_group} &>/dev/null || groupadd -r %{bonnie_group} -g %{bonnie_group_id} &>/dev/null
getent passwd %{bonnie_user} &>/dev/null || \
    useradd -r -u %{bonnie_user_id} -g %{bonnie_group} -d %{_localstatedir}/lib/%{bonnie_user} -s /sbin/nologin \
        -c "Bonnie Account" %{bonnie_user} &>/dev/null || :

# Allow the bonnie user access to mail
gpasswd -a bonnie mail >/dev/null 2>&1

# Make sure our user has the correct home directory
if [ $1 -gt 1 ] ; then
    usermod -d %{_localstatedir}/lib/%{bonnie_user} %{bonnie_user} &>/dev/null || :
fi

%pre -n bonnie-collector
# And allow cyrus access to bonnie.conf
gpasswd -a cyrus bonnie >/dev/null 2>&1
# Allow bonnie access to kolab.conf
gpasswd -a bonnie kolab >/dev/null 2>&1

%pre -n bonnie-dealer
# And allow cyrus access to bonnie.conf
gpasswd -a cyrus bonnie >/dev/null 2>&1

%post -n bonnie-broker
%if 0%{?suse_version}
%fillup_and_insserv -in bonnie-broker
%endif

if [ "$1" == "1" ]; then
%if 0%{?with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add bonnie-broker
%endif
else
%if 0%{?with_systemd}
    /bin/systemctl condrestart bonnie-broker.service >/dev/null 2>&1 || :
%else
    /sbin/service bonnie-broker condrestart
%endif
fi

%preun -n bonnie-broker
if [ "$1" == "0" ]; then
%if 0%{?with_systemd}
    /bin/systemctl --no-reload disable bonnie-broker.service >/dev/null 2>&1 || :
    /bin/systemctl stop bonnie-broker.service >/dev/null 2>&1 || :
%else
    /sbin/service bonnie-broker stop > /dev/null 2>&1
    /sbin/chkconfig --del bonnie-broker
%endif
fi

%post -n bonnie-collector
%if 0%{?suse_version}
%fillup_and_insserv -in bonnie-collector
%endif

if [ "$1" == "1" ]; then
%if 0%{?with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add bonnie-collector
%endif
else
%if 0%{?with_systemd}
    /bin/systemctl condrestart bonnie-collector.service >/dev/null 2>&1 || :
%else
    /sbin/service bonnie-collector condrestart
%endif
fi

%preun -n bonnie-collector
if [ "$1" == "0" ]; then
%if 0%{?with_systemd}
    /bin/systemctl --no-reload disable bonnie-collector.service >/dev/null 2>&1 || :
    /bin/systemctl stop bonnie-collector.service >/dev/null 2>&1 || :
%else
    /sbin/service bonnie-collector stop > /dev/null 2>&1
    /sbin/chkconfig --del bonnie-collector
%endif
fi

%post -n bonnie-worker
%if 0%{?suse_version}
%fillup_and_insserv -in bonnie-worker
%endif

if [ "$1" == "1" ]; then
%if 0%{?with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add bonnie-worker
%endif
else
%if 0%{?with_systemd}
    /bin/systemctl condrestart bonnie-worker.service >/dev/null 2>&1 || :
%else
    /sbin/service bonnie-worker condrestart
%endif
fi

%preun -n bonnie-worker
if [ "$1" == "0" ]; then
%if 0%{?with_systemd}
    /bin/systemctl --no-reload disable bonnie-worker.service >/dev/null 2>&1 || :
    /bin/systemctl stop bonnie-worker.service >/dev/null 2>&1 || :
%else
    /sbin/service bonnie-worker stop > /dev/null 2>&1
    /sbin/chkconfig --del bonnie-worker
%endif
fi

%files
%defattr(-,root,root,-)
%doc conf/bonnie.conf
%attr(0640,%{bonnie_user},%{bonnie_group}) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_prefix}/lib/tmpfiles.d/bonnie.conf
%{python_sitelib}/bonnie/__init__.py*
%{python_sitelib}/bonnie/conf.py*
%{python_sitelib}/bonnie/daemon.py*
%{python_sitelib}/bonnie/logger.py*
%{python_sitelib}/bonnie/translate.py*
%{python_sitelib}/bonnie/utils.py*
%{python_sitelib}/bonnie/plugins/
%attr(0750,%{bonnie_user},%{bonnie_group}) %{_var}/lib/%{name}
%attr(0750,%{bonnie_user},%{bonnie_group}) %{_var}/log/%{name}

%files elasticsearch
%defattr(-,root,root,-)

%files riak
%defattr(-,root,root,-)

%files broker
%defattr(-,root,root,-)
%{_sbindir}/bonnie-broker
%{python_sitelib}/bonnie/broker
%if 0%{?with_systemd}
%{_unitdir}/bonnie-broker.service
%else
%{_initrddir}/bonnie-broker
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/bonnie-broker

%files collector
%defattr(-,root,root,-)
%{_sbindir}/bonnie-collector
%{python_sitelib}/bonnie/collector
%if 0%{?with_systemd}
%{_unitdir}/bonnie-collector.service
%else
%{_initrddir}/bonnie-collector
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/bonnie-collector

%files dealer
%defattr(-,root,root,-)
%{_bindir}/bonnie-dealer
%{_bindir}/bonnie-dealer-sync
%{python_sitelib}/bonnie/dealer

%files worker
%defattr(-,root,root,-)
%{_sbindir}/bonnie-worker
%{python_sitelib}/bonnie/worker
%if 0%{?with_systemd}
%{_unitdir}/bonnie-worker.service
%else
%{_initrddir}/bonnie-worker
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/bonnie-worker

%files wui
%defattr(-,root,root,-)

%changelog
* Sun Jun 17 2018 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3.4-1
- Release of version 0.3.4

* Mon Jan  5 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3.2-1
- Allow the collectors to continue to report state

* Thu Dec 11 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3.1-1
- New upstream release

