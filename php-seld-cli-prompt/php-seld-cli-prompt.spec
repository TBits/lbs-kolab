# remirepo/fedora spec file for php-seld-cli-prompt
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    a19a7376a4689d4d94cab66ab4f3c816019ba8dd
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     Seldaek
%global gh_project   cli-prompt

Name:           php-seld-cli-prompt
Version:        1.0.3
Release:        3.20%{?dist}.kolab_16
Summary:        Allows you to prompt for user input on the command line

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# Autoloader
Source1:        %{gh_project}-autoload.php

BuildArch:      noarch
BuildRequires:  php(language) >= 5.3
# For test
BuildRequires:  php-cli
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)

# From composer.json
#       "php": ">=5.3.0",
Requires:       php(language) >= 5.3.0
# From phpcompatifo report for 1.0.0
Requires:       php-pcre
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(seld/cli-prompt) = %{version}


%description
While prompting for user input using fgets() is quite easy, sometimes you
need to prompt for sensitive information. In these cases, the characters typed
in by the user should not be directly visible, and this is quite a pain to do
in a cross-platform way.

To use this library, you just have to add, in your project:
  require_once '%{_datadir}/php/Seld/CliPrompt/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE1} src/autoload.php


%build
# Nothing


%install
# Restore PSR-0 tree
mkdir -p     %{buildroot}%{_datadir}/php/Seld/CliPrompt
cp -pr src/* %{buildroot}%{_datadir}/php/Seld/CliPrompt/


%check
: Check if our autoloader works
php -r '
require "%{buildroot}%{_datadir}/php/Seld/CliPrompt/autoload.php";
$a = new \Seld\CliPrompt\CliPrompt();
echo "Ok\n";
exit(0);
'


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md composer.json res/example.php
%{_datadir}/php/Seld


%changelog
* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 20 2017 Remi Collet <remi@remirepo.net> - 1.0.3-1
- Update to 1.0.3

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Oct 21 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-2
- switch from symfony/class-loader to fedora/autoloader

* Mon Apr 18 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 10 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1 (no change)

* Wed Oct 14 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-3
- add autoloader

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
