%if 0%{?opensuse_bs}
#!BuildIgnore:  php-mysqlnd
#!BuildIgnore:  roundcubemail-plugin-jqueryui-skin-classic
#!BuildIgnore:  roundcubemail-skin-classic
#!BuildIgnore:  roundcubemail-plugin-managesieve-skin-classic
#!BuildIgnore:  roundcubemail-plugin-acl-skin-classic
#!BuildIgnore:  roundcubemail-skin-classic
#!BuildIgnore:  lighttpd
#!BuildIgnore:  cherokee
#!BuildIgnore:  nginx
#!BuildIgnore:  httpd-itk
%endif

Name:           roundcubemail-skin-plesk-larry
Version:        0.3.3
Release:	    1%{?dist}
Summary:        Plesk Premium Email Web Client skin (Larry Edition)

Group:          Web/Applications
License:        CC-BY-SA
URL:            http://www.kolab.org
Source0:        http://mirror.kolabsys.com/pub/releases/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  roundcubemail(skin-chameleon) >= 0.3.8
BuildRequires:  roundcubemail(skin-chameleon-assets) >= 0.3.8

%if "%{_arch}" != "ppc64" && "%{_arch}" != "ppc64le"
BuildRequires:  nodejs-less
%if 0%{?suse_version} < 1
BuildRequires:  uglify-js
%endif
%else
BuildRequires:  php-lessphp
%endif

BuildRequires:  python

Requires:       roundcubemail(skin-plesk-larry) = %{?epoch:%%{epoch}:}%{version}-%{release}
Requires:       roundcubemail(skin-plesk-larry-assets) = %{?epoch:%%{epoch}:}%{version}-%{release}

%description
This package contains a Kolab Groupware skin for the Roundcube web mail
interface.

%package core
Summary:        Plesk Premium Email Web Client skin (Larry Edition)
Group:          Applications/Internet
Requires:       roundcubemail-core >= 1.1
Requires:       roundcubemail(skin-larry) >= 1.1
Provides:       roundcubemail(skin-plesk-larry) = %{?epoch:%%{epoch}:}%{version}-%{release}

%description core
Kolab skin for Roundcube

%package assets
Summary:        Assets for the Plesk Premium Email skin (Larry Edition)
Group:          Applications/Internet
Requires:       roundcubemail(skin-larry-assets) >= 1.1
Provides:       roundcubemail(skin-plesk-larry-assets) = %{?epoch:%%{epoch}:}%{version}-%{release}

%description assets
Assets for the Plesk Premium Email skin

%prep
%setup -q

%build

%install
mkdir -p \
    %{buildroot}/%{_datadir}/roundcubemail/skins/plesk-larry/ \
    %{buildroot}/%{_datadir}/roundcubemail/public_html/assets/skins/plesk-larry/

cp -av /usr/share/roundcubemail/skins/chameleon/* \
    %{buildroot}/%{_datadir}/roundcubemail/skins/plesk-larry/.

cp -av /usr/share/roundcubemail/public_html/assets/skins/chameleon/* \
    %{buildroot}/%{_datadir}/roundcubemail/public_html/assets/skins/plesk-larry/.

rm -rf skins/plesk-larry/colors.sh

cp -av skins/plesk-larry/* %{buildroot}/%{_datadir}/roundcubemail/skins/plesk-larry/.

orig_dir=%{buildroot}/%{_datadir}/roundcubemail/skins/plesk-larry/
asset_dir=%{buildroot}/%{_datadir}/roundcubemail/public_html/assets/skins/plesk-larry/

# Compress the CSS
for file in `find ${orig_dir} -type f -name "*.less" ! -name "colors.less" | grep -vE "${orig_dir}/(plugins|skins)/"`; do
    asset_loc=$(dirname $(echo ${file} | %{__sed} -e "s|${orig_dir}|$asset_dir|g"))
    %{__mkdir_p} ${asset_loc}
    (
        %{_bindir}/lessc -x ${file} > ${asset_loc}/$(basename ${file} .less).css || \
            cat $(dirname ${file})/colors.less ${file} | %{_bindir}/plessc -r -f=compressed > ${asset_loc}/$(basename ${file} .less).css
        ) && \
        %{__rm} -rf ${file} || \
        %{__mv} -v ${file} ${asset_loc}/$(basename ${file})
done

# Compress the JS, but not the already minified
for file in `find ${orig_dir} -type f -name "*.js" ! -name "*.min.js" | grep -vE "${orig_dir}/(plugins|skins)/"`; do
    asset_loc=$(dirname $(echo ${file} | %{__sed} -e "s|${orig_dir}|$asset_dir|g"))
    %{__mkdir_p} ${asset_loc}
    uglifyjs ${file} > ${asset_loc}/$(basename ${file}) && \
        %{__rm} -rf ${file} || \
        %{__mv} -v ${file} ${asset_loc}/$(basename ${file})
done

# The already minified JS can just be copied over to the assets location
for file in `find ${orig_dir} -type f -name "*.min.js" | grep -vE "${orig_dir}/(plugins|skins)/"`; do
    asset_loc=$(dirname $(echo ${file} | %{__sed} -e "s|${orig_dir}|$asset_dir|g"))
    %{__mkdir_p} ${asset_loc}
    %{__mv} -v ${file} ${asset_loc}/$(basename ${file})
done

# Other assets
for file in $(find ${orig_dir} -type f \
        -name "*.css" -o \
        -name "*.eot" -o \
        -name "*.gif" -o \
        -name "*.ico" -o \
        -name "*.jpg" -o \
        -name "*.png" -o \
        -name "*.svg" -o \
        -name "*.swf" -o \
        -name "*.tif" -o \
        -name "*.ttf" -o \
        -name "*.woff" | \
        grep -vE "${orig_dir}/(plugins|skins)/"
    ); do
    asset_loc=$(dirname $(echo ${file} | %{__sed} -e "s|${orig_dir}|$asset_dir|g"))
    %{__mkdir_p} ${asset_loc}
    %{__mv} -vf ${file} ${asset_loc}/$(basename $file)
done

%files
%defattr(-,root,root,-)

%files core
%defattr(-,root,root,-)
%if 0%{?suse_version}
%dir %{_datadir}/roundcubemail/
%dir %{_datadir}/roundcubemail/skins/
%dir %{_datadir}/roundcubemail/public_html/assets/
%dir %{_datadir}/roundcubemail/public_html/assets/skins/
%endif
%{_datadir}/roundcubemail/skins/plesk-larry/

%files assets
%{_datadir}/roundcubemail/public_html/assets/skins/plesk-larry/

%changelog
* Wed May 30 2018 Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com> - 0.3.3-1
- Release of version 0.3.3
