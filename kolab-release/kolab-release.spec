# The repository type (feature, custom)
%global repository_type feature
%global repository_stage private
%global repository_name kolab
%global repository_version 16

# Fedora or Enterprise Linux?
%if 0%{?fedora} > 0
%global dist_full_name Fedora
%global dist_lower_name fedora
%global dist_tag_prefix f
%global dist_version %{fedora}

%if 0%{?fedora} == 12
%global gpgkey_name constantine
%endif

%if 0%{?fedora} == 13
%global gpgkey_name goddard
%endif

%if 0%{?fedora} == 14
%global gpgkey_name laughlin
%endif

%if 0%{?fedora} == 15
%global gpgkey_name lovelock
%endif

%if 0%{?fedora} == 16
%global gpgkey_name verne
%endif

%if 0%{?fedora} == 17
%global gpgkey_name beefymiracle
%endif

%if 0%{?fedora} == 26
%global gpgkey_name twentysix
%endif

%else
%global dist_full_name Enterprise Linux
%if 0%{?plesk}
%global dist_lower_name plesk-%{?plesk}
%else
%global dist_lower_name redhat
%endif
%global dist_tag_prefix el
%global dist_version %{rhel}
%if 0%{?rhel} == 5
%global gpgkey_name tikanga
%endif
%if 0%{?rhel} == 6
%global gpgkey_name santiago
%endif
%if 0%{?rhel} == 7
%global gpgkey_name maipo
%endif
%if 0%{?rhel} == 8
%global gpgkey_name ootpa
%endif
%endif

# Runtime settings
%global dist_tag %{dist_tag_prefix}%{dist_version}

%if %{?repository_type} == "feature"
%global desc %{dist_full_name} %{dist_version} Kolab %{repository_version}
%if %{?repository_stage} == "public"
%global repository_base_url http://mirror.kolabenterprise.com/pub/%{dist_lower_name}/
%else
%global repository_base_url https://mirror.kolabenterprise.com/%{dist_lower_name}/
%endif
%global repository_full_name %{repository_name}-%{repository_version}
%global repository_tag_name %{repository_name}-%{repository_version}
%else
%global desc %{dist_full_name} %{dist_version} Custom Kolab %{repository_version}
%global repository_base_url https://mirror.kolabenterprise.com/%{dist_lower_name}/custom/
%global repository_full_name custom-%{repository_name}
%global repository_tag_name %{repository_name}
%endif

Summary:    Kolab Systems release files
%if %{repository_stage} == "private"
Name:       %{repository_name}-release
%else
Name:       %{repository_name}-community-release
%endif
Version:    %{repository_version}.%{dist_version}
Release:    13.1%{?dist}.kolab_16
License:    GPLv2
Group:      System Environment/Base
URL:        http://www.kolabenterprise.com
Source0:    kolab-repository-template.repo.tpl
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch
Requires:   %{repository_name}(release) = %{repository_version}

%description
Kolab Systems repository configuration files, such as YUM repository configuration files

%if %{repository_stage} == "public"
%package -n %{repository_full_name}-community-release
Summary:    Kolab release files
Group:      System Environment/Base

Obsoletes:  %{repository_full_name}-release < %{version}
Provides:   %{repository_full_name}-release = %{version}
Provides:   %{repository_name}(release) = %{repository_version}
%if 0%{?rhel}
Requires:   epel-release = %{rhel}
Requires:   pyliblzma
Requires:   yum-plugin-priorities
%endif

%description -n %{repository_full_name}-community-release
This package provides the repository configuration for Kolab
%else
%package -n %{repository_full_name}-release
Summary:    Kolab Enterprise release files by Kolab Systems
Group:      System Environment/Base

Obsoletes:  %{repository_full_name}-release < %{version}
Provides:   %{repository_full_name}-release = %{version}
Provides:   %{repository_name}(release) = %{repository_version}
%if 0%{?rhel}
Requires:   epel-release = %{rhel}
Requires:   pyliblzma
Requires:   yum-plugin-priorities
%endif

Obsoletes:  %{repository_full_name}-community-release < %{version}
Obsoletes:  %{repository_name}-community-release < %{version}
Provides:   %{repository_full_name}-community-release = %{version}
Provides:   %{repository_name}-community-release = %{version}

%description -n %{repository_full_name}-release
This package provides the repository configuration for Kolab Systems' Enterprise version of Kolab

%endif

%if %{?repository_type} == "feature"
%if %{repository_stage} == "public"
%package -n %{repository_full_name}-community-release-development
%else
%package -n %{repository_full_name}-release-development
%endif
Summary:    Development repository definitions
Group:      System Environment/Base
Requires:   %{repository_name}(release) = %{repository_version}
%if 0%{?rhel}
Requires:   epel-release = %{rhel}
Requires:   pyliblzma
Requires:   yum-plugin-priorities
%endif

%if %{repository_stage} == "public"
%description -n %{repository_full_name}-community-release-development
%else
%description -n %{repository_full_name}-release-development
%endif
This package provides the development repository definitions.
%endif

%if %{repository_type} == "feature"
%if %{repository_stage} == "private"
%if %{repository_version} >= 14
%if 0%{?plesk} < 1
%package -n %{repository_full_name}-extras-audit
Summary:    Audit trail packages for Kolab Enterprise %{repository_version}
Group:      System Environment/Base
Requires:   %{repository_name}(release) = %{repository_version}
%if 0%{?rhel}
Requires:   epel-release = %{rhel}
Requires:   pyliblzma
Requires:   yum-plugin-priorities
%endif # 0%{?rhel}

%description -n %{repository_full_name}-extras-audit
Extras repository for Bonnie and Egara on Kolab Enterprise %{repository_version}

%package -n %{repository_full_name}-extras-puppet
Summary:    Puppet 3 packages for Kolab Enterprise %{repository_version}
Group:      System Environment/Base
Requires:   %{repository_name}(release) = %{repository_version}
%if 0%{?rhel}
Requires:   epel-release = %{rhel}
Requires:   pyliblzma
Requires:   yum-plugin-priorities
%endif # 0%{?rhel}

%description -n %{repository_full_name}-extras-puppet
Puppet 3 repository for Kolab Enterprise %{repository_version}

%if 0%{?rhel} >= 6
%package -n %{repository_full_name}-extras-fasttrack
Summary:    Fasttrack packages for Kolab Enterprise %{repository_version}
Group:      System Environment/Base
Requires:   %{repository_name}(release) = %{repository_version}
%if 0%{?rhel}
Requires:   epel-release = %{rhel}
Requires:   pyliblzma
Requires:   yum-plugin-priorities
%endif # 0%{?rhel}

%description -n %{repository_full_name}-extras-fasttrack
Fasttrack repository for Kolab Enterprise %{repository_version}

%package -n %{repository_full_name}-extras-collab
Summary:    Collabora Online packages for Kolab Enterprise %{repository_version}
Group:      System Environment/Base
Requires:   %{repository_name}(release) = %{repository_version}
%if 0%{?rhel}
Requires:   epel-release = %{rhel}
Requires:   pyliblzma
Requires:   yum-plugin-priorities
%endif # 0%{?rhel}

%description -n %{repository_full_name}-extras-collab
Extras repository for Collabora Online on Kolab Enterprise %{repository_version}

%endif # 0%{?rhel} >= 6
%endif # 0%{?plesk} < 1
%endif # %{repository_version} >= 14
%endif # %{repository_stage} == "private"
%endif # %{repository_type} == "feature"

%prep

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}/%{_sysconfdir}

install -d -m 755 %{buildroot}/%{_sysconfdir}/pki/rpm-gpg

##install -m 644 RPM-GPG-KEY-ergo-%{repository}-* %{_sysconfdir}/etc/pki/rpm-gpg/

install -d -m 755 %{buildroot}/%{_sysconfdir}/yum.repos.d

%if %{?repository_type} == "feature"
for repo in release updates updates-testing development; do
    [ "$repo" == "release" ] && status="" || status="-$repo"
    [ "$repo" == "updates-testing" ] && enabled="0" || enabled="1"

    cat %{SOURCE0} | \
        sed \
                -e 's/@@desc@@/%{desc}/g' \
                -e 's/@@dist_full_name@@/%{dist_full_name}/g' \
                -e 's/@@dist_tag@@/%{dist_tag}/g' \
                -e 's/@@dist_version@@/%{dist_version}/g' \
                -e "s/@@enabled@@/$enabled/g" \
                -e 's|@@repository_base_url@@|%{repository_base_url}|g' \
                -e 's/@@repository_full_name@@/%{repository_full_name}/g' \
                -e 's/@@repository_name@@/%{repository_name}/g' \
                -e "s|@@repository_status@@|$repo/|g" \
                -e "s/@@_repository_status@@/$status/g" \
                -e "s/@@_repository_status@@/$status/g" \
                -e 's/@@repository_tag_name@@/%{repository_tag_name}/g' \
        > %{buildroot}/%{_sysconfdir}/yum.repos.d/%{repository_full_name}-$repo.repo
done

%if %{repository_stage} == "private"
%if %{repository_version} >= 14

%if 0%{?plesk} < 1
repos="extras-audit extras-puppet"

%if 0%{?rhel} >= 6
repos="${repos} extras-fasttrack"
%endif # 0%{?rhel} >= 6

%if 0%{?repository_version} >= 16
repos="${repos} extras-collab"
%endif # 0%{?repository_version} >= 16

%endif # 0%{?plesk} < 1

for repo in ${repos}; do
    status="-${repo}"
    cat %{SOURCE0} | \
        sed \
                -e 's/@@desc@@/%{desc}/g' \
                -e 's/@@dist_full_name@@/%{dist_full_name}/g' \
                -e 's/@@dist_tag@@/%{dist_tag}/g' \
                -e 's/@@dist_version@@/%{dist_version}/g' \
                -e "s/@@enabled@@/$enabled/g" \
                -e 's|@@repository_base_url@@|%{repository_base_url}|g' \
                -e 's/@@repository_full_name@@/%{repository_full_name}/g' \
                -e 's/@@repository_name@@/%{repository_name}/g' \
                -e "s|@@repository_status@@|$repo/|g" \
                -e "s/@@_repository_status@@/$status/g" \
                -e "s/@@_repository_status@@/$status/g" \
                -e 's/@@repository_tag_name@@/%{repository_tag_name}/g' \
        > %{buildroot}/%{_sysconfdir}/yum.repos.d/%{repository_full_name}-$repo.repo
done

%endif # %{repository_version} >= 14
%endif # %{repository_stage} == "private"

%else # %if %{?repository_type} == "feature"
    cat %{SOURCE0} | \
        sed \
                -e 's/@@desc@@/%{desc}/g' \
                -e 's/@@dist_full_name@@/%{dist_full_name}/g' \
                -e 's/@@dist_tag@@/%{dist_tag}/g' \
                -e 's/@@dist_version@@/%{dist_version}/g' \
                -e "s/@@enabled@@/1/g" \
                -e 's|@@repository_base_url@@|%{repository_base_url}|g' \
                -e 's/@@repository_full_name@@/%{repository_full_name}/g' \
                -e 's/@@repository_name@@/%{repository_name}/g' \
                -e "s/@@repository_status@@/$repo/g" \
                -e "s/@@_repository_status@@//g" \
                -e 's/@@repository_tag_name@@/%{repository_tag_name}/g' \
        > %{buildroot}/%{_sysconfdir}/yum.repos.d/%{repository_full_name}.repo
%endif # %if %{?repository_type} == "feature"

sed -i \
    -e 's|@@gpgcheck@@|1|g' \
    -e 's|@@gpgkeyname@@|%{gpgkey_name}|g' \
        %{buildroot}/%{_sysconfdir}/yum.repos.d/*.repo

%clean
rm -rf %{buildroot}

%if %{repository_stage} == "public"
%files -n %{repository_full_name}-community-release
%else
%files -n %{repository_full_name}-release
%endif
%defattr(-,root,root,-)
%dir %{_sysconfdir}/yum.repos.d
%if %{?repository_type} == "feature"
%exclude %{_sysconfdir}/yum.repos.d/*development.repo
%endif
%config(noreplace) %{_sysconfdir}/yum.repos.d/*release.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/*updates.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/*updates-testing.repo
%dir %{_sysconfdir}/pki/rpm-gpg
#%{_sysconfdir}/pki/rpm-gpg/*

%if %{?repository_type} == "feature"
%if %{repository_stage} == "public"
%files -n %{repository_full_name}-community-release-development
%else
%files -n %{repository_full_name}-release-development
%endif
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*development.repo
%endif

%if 0%{?plesk} < 1
%if %{repository_type} == "feature"
%if %{repository_stage} == "private"
%if %{repository_version} >= 14
%files -n %{repository_full_name}-extras-audit
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*extras-audit.repo

%files -n %{repository_full_name}-extras-puppet
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*extras-puppet.repo

%if 0%{?rhel} >= 6
%files -n %{repository_full_name}-extras-fasttrack
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*extras-fasttrack.repo
%endif

%endif
%endif
%endif
%endif

%if %{repository_type} == "feature"
%if %{repository_stage} == "private"
%if 0%{?repository_version} >= 16
%if 0%{?plesk} < 1
%files -n %{repository_full_name}-extras-collab
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*extras-collab.repo
%endif
%endif
%endif
%endif

%changelog
* Mon May 14 2018 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 16.7-10
- Add extras-collab for Plesk 17

* Wed Nov  1 2017 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 16.7-2
- Add extras-collab

* Tue Nov 15 2016 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 16.7-1
- Add extras-fasttrack for RHEL 7 too

* Sat Jan 16 2016 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 16.0-1
- Update for Kolab 16
- Also require pyliblzma
- Add fasttrack repository configuration for kolab-14/el6
- Add repository configuration for extras-audit and extras-puppet

* Thu Oct  2 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 14-1
- Kolab Enterprise 14 repository configuration

* Sun Dec  8 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 6-7
- Drop requirement on yum-plugin-priorities, not available in RHEL

* Mon Oct 14 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 6-5
- Make sure yum-plugin-priorities is a required package, documentation
  clearly is insufficient.
- Make sure the default priority is set.

* Thu Apr 11 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 6-4.1
- Correct yum/curl now using the ca and client certificates configured
  in the kolab repository configuration.

* Sat Dec  1 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 6-4
- Correct base_url for private repository stages

* Fri Nov 30 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 6-3
- Correct requires/provides for sub-package
