# Needed for opensuse build system
%if 0%{?opensuse_bs}
#!BuildIgnore:  boa
#!BuildIgnore:  cherokee
#!BuildIgnore:  nginx
#!BuildIgnore:  httpd-itk
#!BuildIgnore:  lighttpd
#!BuildIgnore:  thttpd

#!BuildIgnore:  fedora-logos-httpd
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

Name:       kolab-autodiscover
Version:    0.1
Release:    1%{?dist}
Summary:    Autodiscovery for clients of Kolab Groupware

Group:      Applications/Internet
License:    GPLv3+
URL:        https://kolab.org
Source0:    http://mirror.kolabsys.com/pub/releases/%{name}-%{version}.tar.gz

Requires:   php-Net-LDAP3
BuildArch:  noarch

%description


%prep
%setup -q

%build

%install
%{__mkdir_p} \
    %{buildroot}/%{_ap_sysconfdir}/conf.d/ \
    %{buildroot}/%{_datadir}/%{name}/ \
    %{buildroot}/%{_var}/log/%{name}

%{__cp} -a lib public_html %{buildroot}/%{_datadir}/%{name}/

pushd %{buildroot}/%{_datadir}/%{name}/
ln -s ../../..%{_var}/log/%{name} logs
popd

%{__install} -pm 644 docs/%{name}.conf %{buildroot}/%{_ap_sysconfdir}/conf.d/%{name}.conf

%files
%defattr(-,root,root,-)
%doc docs/*
%dir %{_ap_sysconfdir}
%dir %{_ap_sysconfdir}/conf.d
%config(noreplace) %{_ap_sysconfdir}/conf.d/%{name}.conf
%{_datadir}/%{name}
%attr(0750,%{httpd_user},%{httpd_group}) %{_var}/log/%{name}

%changelog
* Tue Sep  9 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.1-1
- Initial version
