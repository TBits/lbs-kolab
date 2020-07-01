%if 0%{?opensuse_bs}
#!BuildIgnore:  caddy
#!BuildIgnore:  lighttpd
#!BuildIgnore:  nginx
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

%global confdir %{_sysconfdir}/roundcubemail
%global datadir %{_datadir}/roundcubemail
%global plugindir %{datadir}/plugins

Name:           roundcubemail-plugin-sauserprefs
Version:        1.17.1.86
Release:        2.148%{?dist}.kolab_wf
Summary:        Sauserprefs plugin for Roundcube Webmail

Group:          Applications/Internet
License:        AGPLv3+ and GPLv3+
URL:            http://www.kolab.org

# From f3458e5a74372a64ad2387f90ceca33373e259ec
Source0:        %{name}-%{version}.tar.gz

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:      noarch

%if "%{_arch}" != "ppc64" && "%{_arch}" != "ppc64le"
BuildRequires:  nodejs-less
%if 0%{?suse_version} < 1
BuildRequires:  python-cssmin
BuildRequires:  uglify-js
%endif
%endif

BuildRequires:  roundcubemail(skin-elastic)

Requires:       roundcubemail(core) >= 1.4

%description
Adds Spamassassin user preferences to Roundcube

%prep
%setup -q

find . -type f -name "*.less" | while read file; do
    sed -i -e 's|../../../../skins/elastic/styles/|../../../../../../../../usr/share/roundcubemail/skins/elastic/styles/|g' ${file}
done

%build

%install
rm -rf %{buildroot}
mkdir -p \
    %{buildroot}%{confdir}/ \
    %{buildroot}%{plugindir}/sauserprefs

cp -a * %{buildroot}%{plugindir}/sauserprefs

find %{buildroot}%{plugindir}/sauserprefs | sort

pushd %{buildroot}%{plugindir}/sauserprefs
mv config.inc.php.dist %{buildroot}%{confdir}/sauserprefs.inc.php
ln -s ../../../../..%{confdir}/sauserprefs.inc.php config.inc.php
popd

asset_path="%{buildroot}%{datadir}/public_html/assets"

mkdir -p ${asset_path}

orig_dir="%{buildroot}%{datadir}/plugins/"
asset_dir="$asset_path/plugins/"

# Compile and compress the CSS
for file in `find ${orig_dir} -type f -name "*.less" ! -name "colors.less"`; do
    asset_loc=$(dirname $(echo ${file} | %{__sed} -e "s|${orig_dir}|${asset_dir}|g"))
    %{__mkdir_p} ${asset_loc}
    %{_bindir}/lessc --relative-urls -x ${file} > ${asset_loc}/$(basename ${file} .less).css || \
        cat ${file} | %{_bindir}/plessc -r -f=compressed > ${asset_loc}/$(basename ${file} .less).css || :
done
find ${asset_loc} -type f -name "*.css" -empty -delete
find ${asset_loc} -type d -empty -delete

# Compress the CSS
for file in `find $orig_dir -type f -name "*.css"`; do
    asset_loc=$(dirname $(echo ${file} | %{__sed} -e "s|$orig_dir|$asset_dir|g"))
    %{__mkdir_p} ${asset_loc}
    cat ${file} | %{_bindir}/python-cssmin > ${asset_loc}/$(basename ${file}) && \
        %{__rm} -rf ${file} || \
        %{__mv} -v ${file} ${asset_loc}/$(basename ${file})
done

# Compress the JS, but not the already minified
for file in `find $orig_dir -type f -name "*.js" ! -name "*.min.js"`; do
    asset_loc=$(dirname $(echo ${file} | %{__sed} -e "s|$orig_dir|$asset_dir|g"))
    %{__mkdir_p} ${asset_loc}
    uglifyjs ${file} > ${asset_loc}/$(basename ${file}) && \
        %{__rm} -rf ${file} || \
        %{__mv} -v ${file} ${asset_loc}/$(basename ${file})
done

# The already minified JS can just be copied over to the assets location
for file in `find $orig_dir -type f -name "*.min.js"`; do
    asset_loc=$(dirname $(echo ${file} | %{__sed} -e "s|$orig_dir|$asset_dir|g"))
    %{__mkdir_p} ${asset_loc}
    %{__mv} -v ${file} ${asset_loc}/$(basename ${file})
done

# Other assets
for file in $(find $orig_dir -type f \
        -name "*.eot" -o \
        -name "*.gif" -o \
        -name "*.ico" -o \
        -name "*.jpg" -o \
        -name "*.png" -o \
        -name "*.svg" -o \
        -name "*.swf" -o \
        -name "*.tif" -o \
        -name "*.ttf" -o \
        -name "*.woff"
    ); do
    asset_loc=$(dirname $(echo ${file} | %{__sed} -e "s|$orig_dir|$asset_dir|g"))
    %{__mkdir_p} ${asset_loc}
    %{__mv} -vf ${file} ${asset_loc}/$(basename $file)
done

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
%config(noreplace) %attr(0640,root,%{httpd_group}) %{confdir}/sauserprefs.inc.php
%dir %{datadir}
%dir %{plugindir}
%{plugindir}/sauserprefs
%dir %{datadir}/public_html/
%dir %{datadir}/public_html/assets/
%dir %{datadir}/public_html/assets/plugins/
%{datadir}/public_html/assets/plugins/sauserprefs/

%changelog
* Wed Jun  6 2018 Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com> - 1.17.1.86-1
- Release of version 1.17.1.86
