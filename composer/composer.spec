# remirepo/fedora spec file for composer
#
# Copyright (c) 2015-2018 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

# For compatibility with SCL
%undefine __brp_mangle_shebangs

%global gh_commit    b184a92419cc9a9c4c6a09db555a94d441cb11c9
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_branch    1.0-dev
%global gh_owner     composer
%global gh_project   composer
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%global api_version  1.1.0

%global upstream_version 1.6.5
#global upstream_prever  RC

%if 0
# see https://forum.remirepo.net/viewtopic.php?id=3677
%global symfony_prefix php-symfony3
%else
%global symfony_prefix php-symfony
%endif

Name:           composer
Version:        %{upstream_version}%{?upstream_prever:~%{upstream_prever}}
Release:        1.36%{?dist}.kolab_wf
Summary:        Dependency Manager for PHP

Group:          Development/Libraries
License:        MIT
URL:            https://getcomposer.org/
Source0:        %{gh_project}-%{upstream_version}%{?upstream_prever}-%{gh_short}.tgz
Source1:        %{name}-autoload.php
Source2:        %{name}-bootstrap.php
# Profile scripts
Source3:        %{name}.sh
Source4:        %{name}.csh
# Get a git snapshot to retrieve the test suite
Source5:        makesrc.sh

# Use our autoloader, resources path, fix for tests
Patch0:         %{name}-rpm.patch

BuildArch:      noarch
BuildRequires:  php-cli
%if %{with_tests}
BuildRequires:  php-justinrainbow-json-schema5
%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
BuildRequires:  (php-composer(composer/spdx-licenses)   >= 1.2 with  php-composer(composer/spdx-licenses)    <  2)
BuildRequires:  (php-composer(composer/ca-bundle)       >= 1.0 with  php-composer(composer/ca-bundle)        <  2)
BuildRequires:  (php-composer(composer/semver)          >= 1.0 with  php-composer(composer/semver)           <  2)
BuildRequires:  (php-composer(seld/jsonlint)            >= 1.4 with  php-composer(seld/jsonlint)             <  2)
BuildRequires:  (php-composer(seld/phar-utils)          >= 1.0 with  php-composer(seld/phar-utils)           <  2)
BuildRequires:  (php-composer(seld/cli-prompt)          >= 1.0 with  php-composer(seld/cli-prompt)           <  2)
BuildRequires:  (php-composer(psr/log)                  >= 1.0 with  php-composer(psr/log)                   <  2)
%else
BuildRequires:  php-composer(composer/spdx-licenses)    <  2
BuildRequires:  php-composer(composer/spdx-licenses)    >= 1.2
BuildRequires:  php-composer(composer/ca-bundle)        <  2
BuildRequires:  php-composer(composer/ca-bundle)        >= 1.0
BuildRequires:  php-composer(composer/semver)           <  2
BuildRequires:  php-composer(composer/semver)           >= 1.0
BuildRequires:  php-composer(seld/jsonlint)             <  2
BuildRequires:  php-composer(seld/jsonlint)             >= 1.4
BuildRequires:  php-composer(seld/phar-utils)           <  2
BuildRequires:  php-composer(seld/phar-utils)           >= 1.0
BuildRequires:  php-composer(seld/cli-prompt)           <  2
BuildRequires:  php-composer(seld/cli-prompt)           >= 1.0
BuildRequires:  php-composer(psr/log)                   <  2
BuildRequires:  php-composer(psr/log)                   >= 1.0
%endif
BuildRequires:  %{symfony_prefix}-console
BuildRequires:  %{symfony_prefix}-finder
BuildRequires:  %{symfony_prefix}-filesystem
BuildRequires:  %{symfony_prefix}-process
BuildRequires:  php-zip
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "^4.8.35 || ^5.7",
#        "phpunit/phpunit-mock-objects": "^2.3 || ^3.0"
BuildRequires:  php-composer(phpunit/phpunit)           >= 4.8.35
# For autoloader
BuildRequires:  php-composer(fedora/autoloader) >= 0.1.2
BuildRequires:  php-seld-phar-utils >= 1.0.1
BuildRequires:  php-seld-cli-prompt >= 1.0.0-3
BuildRequires:  php-PsrLog          >= 1.0.0-8
%endif

# From composer.json, "require": {
#        "php": "^5.3.2 || ^7.0",
#        "justinrainbow/json-schema": "^3.0 || ^4.0 || ^5.0",
#        "composer/ca-bundle": "^1.0",
#        "composer/semver": "^1.0",
#        "composer/spdx-licenses": "^1.2",
#        "seld/jsonlint": "~1.4",
#        "symfony/console": "^2.7 || ^3.0 || ^4.0",
#        "symfony/finder": "^2.7 || ^3.0 || ^4.0",
#        "symfony/process": "^2.7 || ^3.0 || ^4.0",
#        "symfony/filesystem": "^2.7 || ^3.0 || ^4.0",
#        "seld/phar-utils": "^1.0",
#        "seld/cli-prompt": "^1.0",
#        "psr/log": "^1.0"
Requires:       php(language)                           >= 5.3.2
Requires:       php-cli
Requires:       php-justinrainbow-json-schema5
%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
Requires:       (php-composer(composer/spdx-licenses)   >= 1.2 with  php-composer(composer/spdx-licenses)    <  2)
Requires:       (php-composer(composer/ca-bundle)       >= 1.0 with  php-composer(composer/ca-bundle)        <  2)
Requires:       (php-composer(composer/semver)          >= 1.0 with  php-composer(composer/semver)           <  2)
Requires:       (php-composer(seld/jsonlint)            >= 1.4 with  php-composer(seld/jsonlint)             <  2)
Requires:       (php-composer(seld/phar-utils)          >= 1.0 with  php-composer(seld/phar-utils)           <  2)
Requires:       (php-composer(seld/cli-prompt)          >= 1.0 with  php-composer(seld/cli-prompt)           <  2)
Requires:       (php-composer(psr/log)                  >= 1.0 with  php-composer(psr/log)                   <  2)
%else
Requires:       php-composer(composer/spdx-licenses)    >= 1.2
Requires:       php-composer(composer/spdx-licenses)    <  2
Requires:       php-composer(composer/ca-bundle)        >= 1.0
Requires:       php-composer(composer/ca-bundle)        <  2
Requires:       php-composer(composer/semver)           >= 1.0
Requires:       php-composer(composer/semver)           <  2
Requires:       php-composer(seld/jsonlint)             >= 1.4
Requires:       php-composer(seld/jsonlint)             <  2
Requires:       php-composer(seld/phar-utils)           >= 1.0
Requires:       php-composer(seld/phar-utils)           <  2
Requires:       php-composer(seld/cli-prompt)           >= 1.0
Requires:       php-composer(seld/cli-prompt)           <  2
Requires:       php-composer(psr/log)                   >= 1.0
Requires:       php-composer(psr/log)                   <  2
%endif
Requires:       %{symfony_prefix}-console
Requires:       %{symfony_prefix}-finder
Requires:       %{symfony_prefix}-process
Requires:       %{symfony_prefix}-filesystem
# From composer.json, suggest
#        "ext-zip": "Enabling the zip extension allows you to unzip archives, and allows gzip compression of all internet traffic",
#        "ext-openssl": "Enabling the openssl extension allows you to access https URLs for repositories and packages"
Requires:       php-zip
Requires:       php-openssl
# For our autoloader
Requires:       php-composer(fedora/autoloader)
Requires:       php-seld-phar-utils >= 1.0.1
Requires:       php-seld-cli-prompt >= 1.0.0-3
Requires:       php-PsrLog          >= 1.0.0-8
# From phpcompatinfo
Requires:       php-curl
Requires:       php-date
Requires:       php-dom
Requires:       php-filter
Requires:       php-hash
Requires:       php-iconv
Requires:       php-intl
Requires:       php-json
Requires:       php-libxml
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-phar
Requires:       php-reflection
Requires:       php-simplexml
Requires:       php-spl
Requires:       php-tokenizer
Requires:       php-xsl
Requires:       php-zlib

# Composer library
Provides:       php-composer(composer/composer) = %{version}
# Special internal for Plugin API
Provides:       php-composer(composer-plugin-api) = %{api_version}


%description
Composer helps you declare, manage and install dependencies of PHP projects,
ensuring you have the right stack everywhere.

Documentation: https://getcomposer.org/doc/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1 -b .rpm
find . -name \*.rpm -exec rm {} \; -print

if grep -r '\.\./res'; then
	: Patch need to fixed
	exit 1
fi

cp -p %{SOURCE1} src/Composer/autoload.php
cp -p %{SOURCE2} tests/bootstrap.php
rm src/bootstrap.php

: fix reported version
%if 0%{?gh_date}
DATE=%{gh_date}
DATE=${DATE:0:4}-${DATE:4:2}-${DATE:6:2}
sed -e '/VERSION/s/@package_version@/%{gh_commit}/' \
    -e '/BRANCH_ALIAS_VERSION/s/@package_branch_alias_version@/%{gh_branch}/' \
    -e "/RELEASE_DATE/s/@release_date@/$DATE/" \
    -i src/Composer/Composer.php
%else
sed -e '/BRANCH_ALIAS_VERSION/s/@package_branch_alias_version@//' \
    -i src/Composer/Composer.php
%endif

: check Plugin API version
php -r '
namespace Composer\Plugin;
include "src/Composer/Plugin/PluginInterface.php";
if (version_compare(PluginInterface::PLUGIN_API_VERSION, "%{api_version}")) {
  printf("Plugin API version is %s, expected %s\n", PluginInterface::PLUGIN_API_VERSION, "%{api_version}");
  exit(1);
}'


%build
# Nothing


%install
: Profile scripts
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -m 644 %{SOURCE3} %{SOURCE4} %{buildroot}%{_sysconfdir}/profile.d/

: Library
mkdir -p     %{buildroot}%{_datadir}/php
cp -pr src/* %{buildroot}%{_datadir}/php

: Resources
mkdir -p       %{buildroot}%{_datadir}/%{name}
cp -pr res     %{buildroot}%{_datadir}/%{name}/res
cp -p  LICENSE %{buildroot}%{_datadir}/%{name}/LICENSE

ln -sf %{_datadir}/%{name}/LICENSE LICENSE

: Command
install -Dpm 755 bin/%{name} %{buildroot}%{_bindir}/%{name}


%check
%if %{with_tests}
: Online tests
rm tests/Composer/Test/Util/RemoteFilesystemTest.php

: Known to fail - regression in recent symfony version
sed -e 's/testDevWarningPrevented/SKIP_testDevWarningPrevented/' \
    -e 's/testDevWarningPreventedAlias/SKIP_testDevWarningPreventedAlias/' \
    -i tests/Composer/Test/ApplicationTest.php

: Ensure not used
rm -rf res

: Run test suite
export BUILDROOT=%{buildroot}

# testIntegration may hang on local build
ret=0
for cmd in php php70 php71 php72; do
  if which $cmd; then
    $cmd -d memory_limit=1G %{_bindir}/phpunit \
      --filter '^((?!(testIntegration)).)*$' \
      --include-path %{buildroot}%{_datadir}/php  || ret=1
  fi
done
exit $ret
%else
: Test suite disabled
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md doc
%doc composer.json
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.*
%{_bindir}/%{name}
%{_datadir}/php/Composer
%{_datadir}/%{name}


%changelog
* Fri May  4 2018 Remi Collet <remi@remirepo.net> - 1.6.5-1
- update to 1.6.5

* Mon Apr 16 2018 Remi Collet <remi@remirepo.net> - 1.6.4-1
- update to 1.6.4

* Tue Feb 20 2018 Remi Collet <remi@remirepo.net> - 1.6.3-4
- switch to Symfony2 only

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb  1 2018 Remi Collet <remi@remirepo.net> - 1.6.3-2
- undefine __brp_mangle_shebangs (F28)

* Thu Feb  1 2018 Remi Collet <remi@remirepo.net> - 1.6.3-1
- Update to 1.6.3

* Sun Jan  7 2018 Remi Collet <remi@remirepo.net> - 1.6.2-1
- Update to 1.6.2

* Thu Jan  4 2018 Remi Collet <remi@remirepo.net> - 1.6.1-1
- Update to 1.6.1

* Thu Jan  4 2018 Remi Collet <remi@remirepo.net> - 1.6.0-2
- open https://github.com/composer/composer/pull/6974
  Fix dependency on composer/spdx-licenses
- raise dependency on composer/spdx-licenses 1.2

* Mon Dec 18 2017 Remi Collet <remi@remirepo.net> - 1.5.6-1
- Update to 1.5.6
- switch to symfony package names

* Fri Dec  1 2017 Remi Collet <remi@remirepo.net> - 1.5.5-1
- Update to 1.5.5

* Fri Dec  1 2017 Remi Collet <remi@remirepo.net> - 1.5.4-1
- Update to 1.5.4

* Fri Dec  1 2017 Remi Collet <remi@remirepo.net> - 1.5.3-1
- Update to 1.5.3

* Mon Sep 11 2017 Remi Collet <remi@remirepo.net> - 1.5.2-1
- Update to 1.5.2

* Wed Aug  9 2017 Remi Collet <remi@remirepo.net> - 1.5.1-1
- Update to 1.5.1

* Tue Aug  8 2017 Remi Collet <remi@remirepo.net> - 1.5.0-1
- Update to 1.5.0

* Mon Aug  7 2017 Remi Collet <remi@remirepo.net> - 1.4.3-1
- Update to 1.4.3
- ignore 2 failed tests related to BC break in symfony

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 22 2017 Remi Collet <remi@remirepo.net> - 1.4.2-2
- Update to 1.4.2
- fix autoloader to allow symfony 2 and 3
- raise dependency on justinrainbow/json-schema v5
- open https://github.com/composer/composer/pull/6435 - fix tests

* Fri Mar 10 2017 Remi Collet <remi@remirepo.net> - 1.4.1-1
- Update to 1.4.1

* Wed Mar  8 2017 Remi Collet <remi@remirepo.net> - 1.4.0-1
- Update to 1.4.0
- raise dependency on justinrainbow/json-schema version 3 to 5

* Wed Mar  8 2017 Remi Collet <remi@remirepo.net> - 1.3.3-1
- Update to 1.3.3

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 28 2017 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- update to 1.3.2

* Sat Jan  7 2017 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- update to 1.3.1

* Sat Dec 24 2016 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- update to 1.3.0
- raise dependency on symfony 2.7
- allow justinrainbow/json-schema 4

* Fri Dec 16 2016 Remi Collet <remi@fedoraproject.org> - 1.2.4-2
- fix BR for json-schema, FTBFS from Koschei

* Wed Dec  7 2016 Remi Collet <remi@fedoraproject.org> - 1.2.4-1
- update to 1.2.4

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- update to 1.2.3

* Thu Nov 17 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-2
- add profile scripts so globally installed commands
  will be found in default user path #1394577

* Thu Nov  3 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- update to 1.2.2

* Fri Oct 21 2016 Remi Collet <remi@fedoraproject.org> - 1.2.1-2
- switch from symfony/class-loader to fedora/autoloader

* Mon Sep 12 2016 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- update to 1.2.1

* Tue Jul 19 2016 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0
- switch to justinrainbow/json-schema v2

* Sun Jun 26 2016 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- update to 1.1.3

* Wed Jun  1 2016 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- update to 1.1.2

* Tue May 31 2016 Remi Collet <remi@fedoraproject.org> - 1.1.1-2
- ensure justinrainbow/json-schema v1 is used for the build

* Tue May 17 2016 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1
- add dependency on composer/ca-bundle
- add dependency on psr/log
- bump composer-plugin-api to 1.1.0
- drop dependency on ca-certificates

* Sat Apr 30 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- update to 1.0.3

* Thu Apr 21 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2

* Tue Apr 19 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- add dependency on ca-certificates
- fix patch for RPM path

* Tue Apr  5 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- update to 1.0.0

* Tue Mar 29 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.22.beta2
- update to 1.0.0beta2

* Fri Mar  4 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.21.beta1
- update to 1.0.0beta1

* Tue Feb 23 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.20.201602git4c0e163
- new snapshot
- raise dependency on justinrainbow/json-schema ^1.6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-0.19.20160106git64b0d72
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan  8 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.18.20160106git64b0d72
- add patch for json-schema 1.6, FTBFS detected by Koschei
  open https://github.com/composer/composer/pull/4756
- new snapshot
- raise dependency on seld/jsonlint ^1.4

* Thu Jan  7 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.16.alpha1
- remove duplicated register in autoloader

* Sat Nov 14 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.15.alpha1
- update to 1.0.0alpha11

* Mon Nov  2 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.14.20151030git5a5088e
- new snapshot
- allow symfony 3

* Wed Oct 14 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.13.20151013gita54f84f
- new snapshot
- use autoloader from all dependencies

* Sun Oct 11 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.12.20151007git7a9eb02
- new snapshot
- provide php-composer(composer-plugin-api)
- don't check version in diagnose command
- add dependency on composer/semver
- add dependency on symfony/filesystem

* Tue Sep  8 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.9.20150907git9f6fdfd
- new snapshot
- add LICENSE in application data, as used by the code

* Fri Aug  7 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.8.20150804gitc83650f
- new snapshot

* Tue Jul 21 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.8.20150720git00c2679
- new snapshot
- add dependency on composer/spdx-licenses

* Thu Jul 16 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.7.20150714git92faf1c
- new snapshot
- raise dependency on justinrainbow/json-schema 1.4.4

* Mon Jun 29 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.6.20150626git943107c
- new snapshot
- review autoloader

* Sun Jun 21 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.5.20150620gitd0ff016
- new snapshot
- add missing BR on php-zip
- open https://github.com/composer/composer/pull/4169 for online test

* Mon Jun 15 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.5.20150614git8e9659b
- new snapshot

* Sun Jun  7 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.5.20150605git9fb2d4f
- new snapshot

* Tue Jun  2 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.5.20150531git0ec86be
- new snapshot

* Tue May 26 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.5.20150525git69210d5
- new snapshot
- ensure /usr/share/php is in include_path (for SCL)

* Wed May 13 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.4.20150511gitbc45d91
- new snapshot

* Mon May  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.4.20150503git42a9561
- new snapshot
- add dependencies on seld/phar-utils and seld/cli-prompt

* Mon Apr 27 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.3.20150426git1cb427f
- new snapshot

* Fri Apr 17 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.3.20150415git921b3a0
- new snapshot
- raise dependency on justinrainbow/json-schema ~1.4
- keep upstream shebang with /usr/bin/env (for SCL)

* Thu Apr  9 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.3.20150408git4d134ce
- new snapshot
- lower dependency on justinrainbow/json-schema ~1.3

* Tue Mar 24 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.3.20150324gitc5cd184
- new snapshot
- raise dependency on justinrainbow/json-schema ~1.4

* Thu Mar 19 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2.20150316git829199c
- new snapshot

* Wed Mar  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2.20150302giteadc167
- new snapshot

* Sat Feb 28 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2.20150227git45b1f35
- new snapshot

* Thu Feb 26 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.20150225gite5985a9
- Initial package
