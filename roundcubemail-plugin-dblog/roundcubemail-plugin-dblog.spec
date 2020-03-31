%global roundcube %{_datadir}/roundcubemail
%global roundcube_plugins %{roundcube}/plugins
%global roundcube_conf %{_sysconfdir}/roundcubemail
%global roundcube_log %{_var}/log/roundcubemail
%global roundcube_lib %{_var}/lib/roundcubemail

Name:       roundcubemail-plugin-dblog
Version:    2.0
Release:    1.4%{?dist}.kolab_wf
Summary:    Log to DB plugin for Roundcube Webmail

Group:      Applications/Internet
License:    AGPLv3+ and GPLv3+
URL:        http://www.kolab.org

Source0:    %{name}-%{version}.tar.gz

BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:  noarch

Requires:   roundcubemail >= 0.9

%description
Allows log entries to be created in a database table.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p \
    %{buildroot}%{roundcube_conf} \
    %{buildroot}%{roundcube_plugins}

cp -a dblog %{buildroot}%{roundcube_plugins}
pushd %{buildroot}%{roundcube_plugins}/dblog
mv config.inc.php.dist %{buildroot}%{roundcube_conf}/dblog.inc.php
ln -s ../../../../..%{roundcube_conf}/dblog.inc.php
popd

%post
if [ -f "%{php_inidir}/apc.ini" -o -f "%{php_inidir}/apcu.ini" ]; then
    if [ ! -z "`grep apc.enabled=1 %{php_inidir}/apc{,u}.ini`" ]; then
%if 0%{?fedora} > 15
        /bin/systemctl condrestart httpd.service
%else
    /sbin/service httpd condrestart
%endif
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{roundcube_conf}
%config(noreplace) %attr(0640,root,apache) %{roundcube_conf}/dblog.inc.php
%dir %{roundcube}
%dir %{roundcube_plugins}
%{roundcube_plugins}/dblog

%changelog
* Fri Jun 14 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.0-1
- Initial package version
