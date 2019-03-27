%if 0%{?opensuse_bs}
#!BuildIgnore: lighttpd
#!BuildIgnore: nginx
%endif

%define lock_version() %{1} = %(rpm -q --queryformat "%%{EVR}" %{1})

%{!?php_inidir: %global php_inidir %{_sysconfdir}/php.d}

%if 0%{?suse_version} < 1 && 0%{?fedora} < 1 && 0%{?rhel} < 7
%global with_systemd 0
%else
%global with_systemd 1
%endif

%if 0%{?suse_version}
%global httpd_group www
%global httpd_name apache2
%global httpd_user wwwrun
%else
%if 0%{?plesk}
%global httpd_group roundcube_sysgroup
%global httpd_name httpd
%global httpd_user roundcube_sysuser
%else
%global httpd_group apache
%global httpd_name httpd
%global httpd_user apache
%endif
%endif

%global datadir %{_datadir}/roundcubemail
%global plugindir %{datadir}/plugins
%global confdir %{_sysconfdir}/roundcubemail
%global tmpdir %{_var}/lib/roundcubemail

Name:               roundcubemail-skin-plesk
Version:            0.4
Release:            14.beta1%{?dist}
Summary:            Kolab skin for Roundcube

Group:              Web/Applications
License:            CC-BY-SA
URL:                https://kolabsystems.com

Source0:            %{name}-%{version}-beta1.tar.gz
Source1:            comm.py

BuildArch:          noarch

BuildRequires:      nodejs-less
BuildRequires:      php-lessphp
BuildRequires:      python
BuildRequires:      roundcubemail(skin-elastic)
BuildRequires:      roundcubemail-plugin-libkolab-skin-elastic

Requires:           %lock_version roundcubemail-core
Requires:           %lock_version roundcubemail-plugin-libkolab-skin-elastic

Requires:           roundcubemail(skin-plesk)
Requires:           roundcubemail(skin-plesk-assets)

%description
This package contains the Plesk Premium Email skin for Roundcube

%package core
Summary:            Plesk Premium Email Web Client skin
Group:              Applications/Internet
Requires:           %lock_version roundcubemail-core
Provides:           roundcubemail(skin-plesk) = %{?epoch:%%{epoch}:}%{version}-%{release}

%description core
Kolab skin for Roundcube

%package assets
Summary:            Assets for the Plesk Premium Email skin
Group:              Applications/Internet
Provides:           roundcubemail(skin-plesk-assets) = %{?epoch:%%{epoch}:}%{version}-%{release}

%description assets
Assets for the Plesk Premium Email skin

%prep
%setup -q -n %{name}-%{version}-beta1

rm -rvf kolab/
rm -rvf kolab-now/

find . | sort

find \
    %{datadir}/skins/elastic/ \
    %{datadir}/public_html/assets/skins/elastic/ \
    %{datadir}/plugins/libkolab/skins/elastic/ \
    %{datadir}/public_html/assets/plugins/libkolab/skins/elastic/ \
    -type f | sort | while read file; do
    target_dir=$(dirname ${file} | sed -e 's|%{datadir}|.|g' -e 's|./public_html/assets/|./|g' -e 's|./public_html/assets/plugins/libkolab/|./|g' -e 's/elastic/plesk/g')
    file_name=$(basename ${file})
    if [ ! -d ${target_dir} ]; then
        %{__mkdir_p} ${target_dir}
    fi
    cp -av ${file} ${target_dir}
done

cat ./plugins/libkolab/skins/plesk/libkolab.less

find . | sort

sed -i -e 's/"elastic"/"plesk"/g' \
    $(find skins/plesk/ plugins/libkolab/skins/plesk/ -type f)

find plesk/ -type f | sort | while read file; do
    target_dir="./skins/$(dirname ${file})"
    file_name=$(basename ${file})
    if [ ! -d ${target_dir} ]; then
        %{__mkdir_p} ${target_dir}
    fi
    cp -av ${file} ${target_dir}
done

rm -rvf plesk/

sed -i -e 's/"elastic"/"plesk"/g' plugins/libkolab/skins/plesk/libkolab.less

find . | sort

%build
# Compile and compress the CSS
for file in `find . -type f -name "styles.less" -o -name "print.less" -o -name "embed.less" -o -name "libkolab.less"`; do
    %{_bindir}/lessc --relative-urls ${file} > $(dirname ${file})/$(basename ${file} .less).css

    sed -i \
        -e "s|../../../skins/plesk/images/contactpic.png|../../../../skins/plesk/images/contactpic.png|" \
        -e "s|../../../skins/plesk/images/watermark.jpg|../../../../skins/plesk/images/watermark.jpg|" \
        $(dirname ${file})/$(basename ${file} .less).css

    cat $(dirname ${file})/$(basename ${file} .less).css
done

for orig_dir in "skins/plesk/" "plugins/libkolab/skins/plesk/"; do
    asset_dir="public_html/assets/${orig_dir}"

    # Compress the CSS
    for file in `find ${orig_dir} -type f -name "*.css"`; do
        asset_loc=$(dirname $(echo ${file} | %{__sed} -e "s|${orig_dir}|${asset_dir}|g"))
        %{__mkdir_p} ${asset_loc}
        cat ${file} | %{_bindir}/python-cssmin > ${asset_loc}/$(basename ${file}) && \
            %{__rm} -rf ${file} || \
            %{__mv} -v ${file} ${asset_loc}/$(basename ${file})
    done || :

    # Compress the JS, but not the already minified
    for file in `find ${orig_dir} -type f -name "*.js" ! -name "*.min.js"`; do
        asset_loc=$(dirname $(echo ${file} | %{__sed} -e "s|${orig_dir}|${asset_dir}|g"))
        %{__mkdir_p} ${asset_loc}
        uglifyjs ${file} > ${asset_loc}/$(basename ${file}) && \
            %{__rm} -rf ${file} || \
            %{__mv} -v ${file} ${asset_loc}/$(basename ${file})
    done || :

    # The already minified JS can just be copied over to the assets location
    for file in `find ${orig_dir} -type f -name "*.min.js"`; do
        asset_loc=$(dirname $(echo ${file} | %{__sed} -e "s|${orig_dir}|${asset_dir}|g"))
        %{__mkdir_p} ${asset_loc}
        %{__mv} -v ${file} ${asset_loc}/$(basename ${file})
    done || :

    # Other assets
    for file in $(find ${orig_dir} -type f \
            -name "*.eot" -o \
            -name "*.gif" -o \
            -name "*.ico" -o \
            -name "*.jpg" -o \
            -name "*.mp3" -o \
            -name "*.png" -o \
            -name "*.svg" -o \
            -name "*.swf" -o \
            -name "*.tif" -o \
            -name "*.ttf" -o \
            -name "*.woff" -o \
            -name "*.woff2"
        ); do
        asset_loc=$(dirname $(echo ${file} | %{__sed} -e "s|${orig_dir}|${asset_dir}|g"))
        %{__mkdir_p} ${asset_loc}
        %{__mv} -vf ${file} ${asset_loc}/$(basename $file)
    done || :

    # Purge empty directories
    find ${orig_dir} -type d -empty -delete || :
done

find . | sort

%install
%{__rm} -rvf %{buildroot}
%{__mkdir_p} \
    %{buildroot}%{datadir}/public_html/assets/skins/ \
    %{buildroot}%{datadir}/skins/

cp -av skins/plesk/ %{buildroot}%{datadir}/skins/.
cp -av public_html/assets/skins/plesk/ %{buildroot}%{datadir}/public_html/assets/skins/plesk/
cp -av plugins/ %{buildroot}%{datadir}/plugins
cp -av public_html/assets/plugins/ %{buildroot}%{datadir}/public_html/assets/.

# Workaround for watermark.html
cp -av skins/plesk/watermark.html %{buildroot}%{datadir}/public_html/assets/skins/plesk/

%files
%defattr(-,root,root,-)

%files core
%defattr(-,root,root,-)
%{datadir}/skins/plesk/
%{datadir}/plugins/libkolab/

%files assets
%defattr(-,root,root,-)
%{datadir}/public_html/assets/skins/plesk/
%{datadir}/public_html/assets/plugins/libkolab/

%changelog
* Tue Sep 18 2018 Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com> - 0.4-14.beta1
- Improvements to moving the about button to settings

* Mon Aug 27 2018 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.4-11.beta1
- Update to beta release, rebuild against core Elastic skin updates

* Thu Jul 12 2018 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.4-10.alpha0
- Rebuild against core Elastic skin updates

* Tue Jun  5 2018 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.4-9.alpha0
- Updates

* Tue May 29 2018 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.4-7.alpha0
- Updates

* Tue May 22 2018 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.4-6.alpha0
- Updates

* Wed May 16 2018 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.4-5.alpha0
- Rebuild against latest elastic skin developments

* Tue May  1 2018 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.4-1.alpha0
- Initial package
