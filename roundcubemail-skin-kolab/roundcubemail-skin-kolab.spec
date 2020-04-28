%if 0%{?opensuse_bs}
#!BuildIgnore: lighttpd
#!BuildIgnore: nginx
%endif

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

Name:               roundcubemail-skin-kolab
Version:            0.4.1
Release:            9.23%{?dist}.kolab_16
Summary:            Kolab skin for Roundcube

Group:              Web/Applications
License:            CC-BY-SA
URL:                https://kolabsystems.com
Source0:            %{name}-%{version}.tar.gz
Source1:            comm.py

BuildArch:          noarch

BuildRequires:      nodejs-less
BuildRequires:      php-lessphp
BuildRequires:      python
BuildRequires:      roundcubemail(skin-elastic)
BuildRequires:      roundcubemail-plugin-libkolab-skin-elastic

Requires:           roundcubemail-core
Requires:           roundcubemail-plugin-libkolab-skin-elastic
Provides:           roundcubemail(skin-kolab) = %{version}-%{release}

%description
This package contains the Kolab Groupware skin for Roundcube

%prep
%setup -q -n %{name}-%{version}/

rm -rvf base4kids/
rm -rvf contargo/
rm -rvf now/
rm -rvf plesk/

find . | sort

find \
    %{datadir}/skins/elastic/ \
    %{datadir}/public_html/assets/skins/elastic/ \
    %{datadir}/plugins/libkolab/skins/elastic/ \
    %{datadir}/public_html/assets/plugins/libkolab/skins/elastic/ \
    -type f | sort | while read file; do
    target_dir=$(dirname ${file} | sed -e 's|%{datadir}|.|g' -e 's|./public_html/assets/|./|g' -e 's|./public_html/assets/plugins/libkolab/|./|g' -e 's/elastic/kolab/g')
    file_name=$(basename ${file})
    if [ ! -d ${target_dir} ]; then
        %{__mkdir_p} ${target_dir}
    fi
    cp -av ${file} ${target_dir}
done

find . | sort

sed -i -e 's/"elastic"/"kolab"/g' \
    $(find skins/kolab/ plugins/libkolab/skins/kolab/ -type f)

find kolab/ -type f | sort | while read file; do
    target_dir="./skins/$(dirname ${file})"
    file_name=$(basename ${file})
    if [ ! -d ${target_dir} ]; then
        %{__mkdir_p} ${target_dir}
    fi
    cp -av ${file} ${target_dir}
done

rm -rvf kolab/

sed -i -e 's/"elastic"/"kolab"/g' plugins/libkolab/skins/kolab/libkolab.less

find . | sort

%build

# Compile and compress the CSS
for file in `find . -type f -name "styles.less" -o -name "print.less" -o -name "embed.less" -o -name "libkolab.less"`; do
    %{_bindir}/lessc --relative-urls ${file} > $(dirname ${file})/$(basename ${file} .less).css

    sed -i \
        -e "s|../../../skins/kolab/images/contactpic.png|../../../../skins/kolab/images/contactpic.png|" \
        -e "s|../../../skins/kolab/images/watermark.jpg|../../../../skins/kolab/images/watermark.jpg|" \
        $(dirname ${file})/$(basename ${file} .less).css
done

for orig_dir in "skins/kolab/" "plugins/libkolab/skins/kolab/"; do
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

cp -av skins/kolab/ %{buildroot}%{datadir}/skins/.
cp -av public_html/assets/skins/kolab/ %{buildroot}%{datadir}/public_html/assets/skins/kolab/
cp -av plugins/ %{buildroot}%{datadir}/plugins
cp -av public_html/assets/plugins/ %{buildroot}%{datadir}/public_html/assets/.

# Workaround for watermark.html
cp -av skins/kolab/watermark.html %{buildroot}%{datadir}/public_html/assets/skins/kolab/

%files
%{datadir}/skins/kolab/
%{datadir}/public_html/assets/skins/kolab/

%{datadir}/plugins/libkolab/
%{datadir}/public_html/assets/plugins/libkolab/

%changelog
* Mon Jul  1 2019 Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com> - 0.4.1-5
- Rebuild against core updates

* Mon Jun  3 2019 Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com> - 0.4.1-3
- Rebuild against core updates

* Wed May 15 2019 Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com> - 0.4.1-1
- Release version 0.4.1

* Tue May  7 2019 Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com> - 0.4.0-1
- Release of version 0.4.0

* Sat Jan 19 2019 Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com> - 0.4-16.beta1
- Rebuild against core updates

* Mon Oct 29 2018 Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com> - 0.4-15.beta1
- Rebuild against core updates

* Tue Sep 18 2018 Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com> - 0.4-14.beta1
- Check in beta release

* Thu Jul 12 2018 Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com> - 0.4-13
- Small alignment fixes

* Thu May 31 2018 Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com> - 0.4-12
- Updates

* Tue May 29 2018 Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com> - 0.4-11
- Updates

* Wed May 16 2018 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.4-10
- Updates to the Kolab version of the responsive Elastic skin for Roundcube

* Mon Apr 30 2018 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.0.1-5
- Initial package
