%define git_short_version_hash 14765d3
%define git_full_version_hash 14765d36f83acac0a109a047244aaa6fd8e081ea

Summary: A collection of PHP utility classes
Name: libphutil
Version: 20151230.git%{git_short_version_hash}
Release: 2%{?dist}
License: ASL 2.0
URL: http://www.phabricator.com/docs/libphutil/
Source0: https://github.com/phacility/libphutil/archive/libphutil-%{git_short_version_hash}.tar.gz
BuildArch: noarch

Requires: php-common >= 5

%description
A collection of PHP utility classes used with phabricator

%prep
%setup -q -n libphutil-%{git_full_version_hash}

%build

%install
# copy libphutil to the buildroot
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a * %{buildroot}%{_datadir}/%{name}/



%files
%doc %{_datadir}/%{name}/README.md
%doc %{_datadir}/%{name}/LICENSE
%doc %{_datadir}/%{name}/NOTICE
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/externals
%dir %{_datadir}/%{name}/externals/includes
%{_datadir}/%{name}/resources
%{_datadir}/%{name}/scripts
%{_datadir}/%{name}/src
%{_datadir}/%{name}/support
%{_datadir}/%{name}/externals/includes/README
%{_datadir}/%{name}/externals/jsonlint

%changelog
* Wed Feb 25 2015 Tim Flink <tflink@fedoraproject.org> - 20150211.git9e0ea2c-2
- un-removing bundled jsonlint because the bundled version isn't compatible with upstream

* Wed Feb 11 2015 Tim Flink <tflink@fedoraproject.org> - 20150211.git9e0ea2c-1
- Updating to latest upstream git

* Sat Jan 17 2015 Vladimir Rusinov <vladimir@greenmice.info> - 20141204.git549aa1b-2
- remove bundled jsonlint

* Thu Dec 04 2014 Tim Flink <tflink@fedoraproject.org> - 20141204.git549aa1b-1
- updating to latest upstream git

* Tue Sep 02 2014 Tim Flink <tflink@fedoraproject.org> - 20140902.git2de6440-1
- updating to latest upstream git

* Mon Jul 21 2014 Tim Flink <tflink@fedoraproject.org> - 20140721.gitefc2cc5-1
- updating to latest upstream git

* Sun May 18 2014 Tim Flink <tflink@fedoraproject.org> - 20140518.git1add454-1
- updating to latest upstream git

* Thu Jan 23 2014 Tim Flink <tflink@fedoraproject.org> - 20140123.git86d651f-1
- updating to latest git

* Tue Dec 10 2013 Tim Flink <tflink@fedoraproject.org> - 20131210.git69490c5-1
- updating to latest git

* Wed Oct 30 2013 Tim Flink <tflink@fedoraproject.org> - 20131030.gitba9c942-1
- Initial package
