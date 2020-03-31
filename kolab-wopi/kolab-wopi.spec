%define lock_version() %{1}%{?_isa} = %(rpm -q --queryformat "%{VERSION}" %{1})

%global ssl_pem_file %{_sysconfdir}/pki/%{name}/%{name}.pem

%{?!_unitdir: %global _unitdir /usr/lib/systemd/system}

Name:               kolab-wopi
Version:            0.0.1
Release:	        3.53%{?dist}.kolab_wf
Summary:            Web Application Open Platform Interface for Kolab

Group:              Applications/Web
License:            AGPLv3+
URL:                https://kolab.org
Source0:            kolab_wopi-%{version}.tar.gz
Source1:            %{name}.service

BuildRequires:      erlang-asn1
BuildRequires:      erlang-erts
BuildRequires:      erlang-sasl
BuildRequires:      erlang-ssl

Requires(post):     systemd-units
Requires(postun):   systemd-units
Requires(preun):    coreutils
Requires(preun):    systemd-units

Requires:           %lock_version erlang-asn1
Requires:           %lock_version erlang-erts
Requires:           %lock_version erlang-sasl
Requires:           %lock_version erlang-ssl

%description
This is the collaborative editing WOPI interface for Kolab

%prep
%setup -q -c %{name}-%{version}

%build

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}/opt/
cp -av * %{buildroot}/opt/.

mkdir -p %{buildroot}/%{_unitdir}
%{__install} -p -m 644 %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}.service

mkdir -p \
    %{buildroot}/%{_sysconfdir}/%{name} \
    %{buildroot}/%{_sysconfdir}/pki/%{name}

touch %{buildroot}%{ssl_pem_file}

pushd %{buildroot}/opt/kolab_wopi/releases/%{version}/
mv -v sys.config %{buildroot}/%{_sysconfdir}/%{name}/sys.config
mv -v vm.args %{buildroot}/%{_sysconfdir}/%{name}/vm.args
ln -svf ../../../..%{_sysconfdir}/%{name}/sys.config sys.config
ln -svf ../../../..%{_sysconfdir}/%{name}/vm.args vm.args
popd

sed -i \
    -e 's|/etc/ssl/certs/acme.key|%{ssl_pem_file}|g' \
    -e 's|/etc/ssl/certs/acme.crt|%{ssl_pem_file}|g' \
    %{buildroot}/%{_sysconfdir}/%{name}/sys.config

%postun
%systemd_postun

%post
%systemd_post %{name}.service

# Create SSL certificates
  exec > /dev/null 2> /dev/null

if [ ! -z "%{ssl_pem_file}" -a -z "$(cat %{ssl_pem_file})" ]; then
    %{__rm} -f "%{ssl_pem_file}" || :
fi

if [ ! -f %{ssl_pem_file} -a -d "%{_sysconfdir}/pki/tls/certs" ]; then
    pushd %{_sysconfdir}/pki/tls/certs
    umask 077
    %{__cat} << EOF | make %{name}.pem
--
SomeState
SomeCity
SomeOrganization
SomeOrganizationalUnit
localhost.localdomain
root@localhost.localdomain
EOF

    %{__chmod} 640 %{name}.pem
    mv %{name}.pem %{ssl_pem_file}
    popd
fi


%preun
%systemd_preun %{name}.service

%posttrans
test -f /etc/sysconfig/guam-disable-posttrans || \
    systemctl try-restart %{name}.service 2>&1 || :

%files
%config(noreplace) %{_sysconfdir}/%{name}/sys.config
%config(noreplace) %{_sysconfdir}/%{name}/vm.args
%attr(0640,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{ssl_pem_file}

%{_unitdir}/%{name}.service
/opt/kolab_wopi

%changelog
* Mon May 29 2017 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.0.1-2
- Add systemd script
- Add configuration semantics
- First package
