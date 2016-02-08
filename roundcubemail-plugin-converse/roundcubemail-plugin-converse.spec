%global roundcube %{_datadir}/roundcubemail
%global roundcube_plugins %{roundcube}/plugins
%global roundcube_conf %{_sysconfdir}/roundcubemail
%global roundcube_log %{_var}/log/roundcubemail
%global roundcube_lib %{_var}/lib/roundcubemail

Name:       roundcubemail-plugin-converse
Version:    0.0
Release:    0.1.dev20140214.git14fe73%{?dist}
Summary:    XMPP-based chat plugin for Roundcube Webmail

Group:      Applications/Internet
License:    AGPLv3+ and GPLv3+
URL:        http://www.kolab.org

# From GIT 14fe735080712b66cc89a709d16d776d205cccc8
Source0:    %{name}-%{version}.tar.gz

BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:  noarch

Requires:   roundcubemail >= 0.9

%description
Adds XMPP-based chat to Roundcube

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p \
    %{buildroot}%{roundcube_conf} \
    %{buildroot}%{roundcube_plugins}/converse

cp -av * %{buildroot}%{roundcube_plugins}/converse/.
pushd %{buildroot}%{roundcube_plugins}/converse
mv config.inc.php.dist %{buildroot}%{roundcube_conf}/converse.inc.php
ln -s ../../../../..%{roundcube_conf}/converse.inc.php
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
%config(noreplace) %attr(0640,root,apache) %{roundcube_conf}/converse.inc.php
%dir %{roundcube}
%dir %{roundcube_plugins}
%{roundcube_plugins}/converse

%changelog
* Fri Feb 14 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.0-0.1.git
- Initial package version
