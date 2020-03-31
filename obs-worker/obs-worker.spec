Name:           obs-worker
Summary:        The Open Build Service -- Worker Component
License:        GPL-2.0 and GPL-3.0
Group:          Productivity/Networking/Web/Utilities
Version:        2.5.6
Release:        2.4%{?dist}.kolab_wf
Url:            http://en.opensuse.org/Build_Service
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        obsworker.sysvinit
Source1:        obs-server.sysconfig

Requires:       bash
Requires:       binutils
Requires:       bsdtar
Requires:       cpio
Requires:       curl
Requires:       perl-Compress-Zlib
Requires:       perl-TimeDate
Requires:       perl-XML-Parser
Requires:       psmisc
Requires:       screen

%description
The Open Build Service (OBS) backend is used to store all sources and binaries. It also
calculates the need for new build jobs and distributes it.

%prep

%build

%install
mkdir -p \
    %{buildroot}%{_initddir} \
    %{buildroot}%{_sysconfdir}/sysconfig/ \
    %{buildroot}/%{_var}/cache/obs/ \
    %{buildroot}/%{_var}/lib/obs/

install -m 0755 %{SOURCE0} \
    %{buildroot}%{_initddir}/obsworker

install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/obs-server



%check

%pre
getent group obsrun >/dev/null || groupadd -r obsrun
getent passwd obsrun >/dev/null || \
    /usr/sbin/useradd -r -g obsrun -d /var/lib/obs -s %{_sbin}/nologin \
    -c "User for build service backend" obsrun
exit 0

%post
chkconfig --add obsworker >/dev/null 2>&1 || :
systemctl daemon-reload >/dev/null 2>&1 || :

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/obs-server
%{_initddir}/obsworker
%attr(0755,obsrun,obsrun) %{_var}/cache/obs/
%attr(0755,obsrun,obsrun) %{_var}/lib/obs/

%changelog
* Thu Jul 16 2015 Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com> - 2.5.6-2.1
- Initial package
