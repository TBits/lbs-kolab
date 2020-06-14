%if 0%{?opensuse_bs}
#!BuildIgnore:  cherokee
#!BuildIgnore:  httpd-itk
#!BuildIgnore:  lighttpd
#!BuildIgnore:  nginx

#!BuildIgnore:  php-mysql
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

Name:           copenhagen
Version:        0.0.2
Release:        1.370%{?dist}.kolab_wf
Summary:        Copenhagen for OpenChange

BuildArch:      noarch

Group:          Applications/Productivity
License:        AGPLv3+
URL:            https://kolab.org/about/copenhagen
Source0:        copenhagen-0.0.2.tar.gz

BuildRequires:  php-kolabformat
BuildRequires:  php-pear(HTTP_Request2)
BuildRequires:  php-phpunit-PHPUnit
BuildRequires:  roundcubemail-core
BuildRequires:  roundcubemail-plugin-libcalendaring
BuildRequires:  roundcubemail-plugin-libkolab

Requires:       php-pear(HTTP_Request2)
Requires:       roundcubemail-core
Requires:       roundcubemail-plugin-libcalendaring
Requires:       roundcubemail-plugin-libkolab

%description
Copenhagen is a RESTful API for Kolab Groupware, primarily
intended to provide OpenChange with access to Kolab
payload, for supporting native Outlook (E)MAPI clients.

%prep
%setup -q

%build

%install
mkdir -p \
    %{buildroot}/%{_datadir}/%{name} \
    %{buildroot}/%{_var}/lib/%{name} \
    %{buildroot}/%{_var}/log/%{name}

cp -a * %{buildroot}/%{_datadir}/%{name}

pushd %{buildroot}/%{_datadir}/%{name}
ln -s ../../..%{_var}/lib/%{name} temp
ln -s ../../..%{_var}/log/%{name} logs
popd

%files
%defattr(-,root,root,-)
%doc README.md doc/
%attr(750,%{httpd_user},%{httpd_group}) %{_var}/lib/%{name}
%attr(750,%{httpd_user},%{httpd_group}) %{_var}/log/%{name}
%{_datadir}/%{name}

%changelog
* Mon Apr 20 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.0.1-1
- First package
