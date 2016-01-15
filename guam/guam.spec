%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global debug_package %{nil}

%global realname kolab_guam

%global guam_user guam
%global guam_group guam

Name:               guam
Version:            0.7.0
Release:            1%{?dist}
Summary:            A Smart Reverse IMAP Proxy

Group:              System Environment/Daemons
License:            GPLv3+
URL:                https://kolab.org/about/guam

# From 3e4a3da61124e9c79b7f7f49516e6e86aa072051
Source0:            guam-0.7.0.tar.gz

BuildRequires:      erlang
BuildRequires:      erlang-eimap >= 0.1.5
BuildRequires:      erlang-goldrush
BuildRequires:      erlang-lager >= 2.1.0
BuildRequires:      erlang-rebar >= 2.5.1

Requires(pre):      shadow-utils
Requires(postun):   shadow-utils

Requires:           erlang
Requires:           erlang-eimap >= 0.1.2
Requires:           erlang-goldrush
Requires:           erlang-lager >= 2.1.0

%description
Guam is a smart, unjustly outcasted Reverse IMAP Proxy that lives at
the perimeter of your IMAP environment.

%prep
%setup -q

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
    %{buildroot}%{_var}/log/

cp -a rel/%{realname} %{buildroot}/opt/.

cat > %{buildroot}%{_sbindir}/guam << EOF
#!/bin/bash
exec /opt/kolab_guam/bin/kolab_guam \$*
EOF

mv %{buildroot}/opt/%{realname}/releases/*/sys.config \
    %{buildroot}%{_sysconfdir}/guam/sys.config

ln -s ../../../..%{_sysconfdir}/%{name}/sys.config \
    $(ls -1d %{buildroot}/opt/%{realname}/releases/*/)/sys.config

mv %{buildroot}/opt/%{realname}/log %{buildroot}%{_var}/log/guam
ln -s ../..%{_var}/log/guam %{buildroot}/opt/%{realname}/log

%check
rebar skip_deps=true eunit -v

%pre
if [ $1 == 1 ]; then
    /usr/sbin/groupadd --system %{guam_group} 2> /dev/null || :
    /usr/sbin/useradd -c "Guam Service" -d /opt/kolab_guam -g %{guam_group} \
        -s /sbin/nologin --system %{guam_user} 2> /dev/null || :
fi

%postun
if [ $1 == 0 ]; then
    /usr/sbin/userdel %{guam_user} 2>/dev/null || :
    /usr/sbin/groupdel %{guam_group} 2>/dev/null || :
fi

%files
%attr(0750,root,root) %{_sbindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/sys.config
%attr(0640,%{guam_user},%{guam_group}) %{_var}/log/%{name}/
/opt/%{realname}/

%changelog
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
