%if 0%{?opensuse_bs}
#!BuildIgnore:  python-jinja2-26
%endif

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}

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

%global bonnie_user bonnie
%global bonnie_user_id 415
%global bonnie_group bonnie
%global bonnie_group_id 415

Name:           bonnie-flask
Version:        0.3
Release:        1.41%{?dist}.kolab_wf
Summary:        Flask-based Web UI for Bonnie

Group:          Applications/System
License:        GPLv3+
URL:            https://kolab.org/about/bonnie

# From 75641e448a182e4205f594a7f8cdbb4f21f25215
Source0:        http://mirror.kolabsys.com/pub/releases/bonnie-flask-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-flask
BuildRequires:  pytz
BuildRequires:  python-setuptools
BuildRequires:  python-sqlalchemy
BuildRequires:  python-twisted-core

Requires:       mod_wsgi
Requires:       pykolab-xml
Requires:       python-elasticsearch
Requires:       python-flask
Requires:       python-flask-babel
Requires:       python-flask-bootstrap
Requires:       python-flask-httpauth
Requires:       python-flask-login
Requires:       python-flask-script
Requires:       python-flask-sqlalchemy
Requires:       python-itsdangerous
Requires:       python-riak
Requires:       pytz

%description
Flask-based Web UI for Bonnie

%prep
%setup -q

%build

%install
mkdir -p \
    %{buildroot}/%{_sysconfdir}/bonnie-flask/ \
    %{buildroot}%{_ap_sysconfdir}/conf.d/ \
    %{buildroot}/%{_datadir}/bonnie-flask/ \
    %{buildroot}/%{_var}/lib/bonnie/

cp -a app/ bonnie-flask.wsgi config.py run.py %{buildroot}/%{_datadir}/bonnie-flask/.
cp -a config/bonnie-flask.conf %{buildroot}/%{_sysconfdir}/bonnie-flask/bonnie-flask.conf
pushd %{buildroot}/%{_datadir}/bonnie-flask/
ln -s ../../..%{_sysconfdir}/bonnie-flask/ config
popd

cp -a bonnie-flask.conf %{buildroot}%{_ap_sysconfdir}/conf.d/

%pre
# Add the kolab user and group accounts
getent group %{bonnie_group} &>/dev/null || groupadd -r %{bonnie_group} -g %{bonnie_group_id} &>/dev/null
getent passwd %{bonnie_user} &>/dev/null || \
    useradd -r -u %{bonnie_user_id} -g %{bonnie_group} -d %{_localstatedir}/lib/%{bonnie_user} -s /sbin/nologin \
        -c "Bonnie Account" %{bonnie_user} &>/dev/null || :

# Make sure our user has the correct home directory
if [ $1 -gt 1 ] ; then
    usermod -d %{_localstatedir}/lib/%{bonnie_user} %{bonnie_user} &>/dev/null || :
fi

%files
%defattr(-,root,root,-)
%doc README.md
%{_ap_sysconfdir}/conf.d/bonnie-flask.conf
%dir %{_sysconfdir}/bonnie-flask/
%attr(0640,%{bonnie_user},%{bonnie_group}) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_datadir}/bonnie-flask
%attr(0750,%{bonnie_user},%{bonnie_group}) %{_var}/lib/bonnie

%changelog
* Fri May 15 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.3-1
- Third package

* Thu Dec  4 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.2-1
- Second package

* Mon Oct 13 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.1-1
- First package
