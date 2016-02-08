%define git_short_version_hash b3e68c9
%define git_full_version_hash b3e68c9f179318d65b6a2512efa6830e0362de8e

Summary: A command line interface to Phabricator
Name: arcanist
Version: 20151230.git%{git_short_version_hash}
Release: 1%{?dist}
License: ASL 2.0
URL: http://www.phabricator.com/docs/arcanist/
Source0: https://github.com/phacility/arcanist/archive/arcanist-%{git_short_version_hash}.tar.gz
BuildArch: noarch

Requires: php-common >= 5
Requires: libphutil

%description
A command line interface to Phabricator


%prep
%setup -q -n arcanist-%{git_full_version_hash}


%build


%install
# copy arcanist to the buildroot
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a * %{buildroot}%{_datadir}/%{name}/

# symlink the bin
mkdir -p %{buildroot}%{_bindir}
pushd %{buildroot}%{_bindir}
ln -s %{_datadir}/%{name}/bin/arc
popd

%files
%{_datadir}/%{name}
%{_bindir}/arc


%changelog
* Wed Feb 11 2015 Tim Flink <tflink@fedoraproject.org> - 20151211.git3f132f4-1
- updating to latest git

* Thu Dec 04 2014 Tim Flink <tflink@fedoraproject.org> - 20141204.gitb46d4ed-1
- updating to latest git

* Tue Sep 02 2014 Tim Flink <tflink@fedoraproject.org> - 20140902.gitc8f1513-1
- updating to latest git

* Mon Jul 21 2014 Tim Flink <tflink@fedoraproject.org> - 20140721.gitef18ae0-1
- updating to latest git

* Sun May 18 2014 Tim Flink <tflink@fedoraproject.org> - 20140518.git0468be3-1
- updating to latest git

* Thu Jan 23 2014 Tim Flink <tflink@fedoraproject.org> - 20140123.git2c2c566-1
- updating to latest git

* Tue Dec 10 2013 Tim Flink <tflink@fedoraproject.org> - 20131210.gite0b4eef-1
- updating to latest git

* Wed Oct 30 2013 Tim Flink <tflink@fedoraproject.org> - 20131030.gitaabbdbd-1
- Initial package
