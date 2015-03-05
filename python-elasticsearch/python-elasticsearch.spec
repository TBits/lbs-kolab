%{!?__python2: %global __python2 %(which python)}
%{!?python2_sitelib: %global python2_sitelib %{python_sitelib}}

%global tarball_name elasticsearch 

Name:           python-elasticsearch
Version:        1.0.0
Release:        1%{?dist}
Summary:        Client for Elasticsearch 

Group:          Development/Languages
License:        ASL 2.0
URL:            https://github.com/elasticsearch/elasticsearch-py
Source0:        https://pypi.python.org/packages/source/e/%{tarball_name}/%{tarball_name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel python-setuptools
Requires:       python-thrift python-urllib3

%description
Low level client for Elasticsearch. It's goal is to provide common ground
for all Elasticsearch-related code in Python. The client's features include:

- Translating basic Python data types to and from json
- Configurable automatic discovery of cluster nodes
- Persistent connections
- Load balancing (with pluggable selection strategy) across all available nodes
- Failed connection penalization (time based - failed connections won't be
  retried until a timeout is reached)
- Thread safety
- Pluggable architecture

%prep
%setup -qn %{tarball_name}-%{version}
rm -fr %{tarball_name}.egg-info

%build
%{__python2} setup.py build


%install
rm -rf %{buildroot}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%files
%{python2_sitelib}/*
%doc README LICENSE

%changelog
* Mon Apr 14 2014 Daniel Bruno <dbruno@fedoraproject.org> - 1.0.0-1
- Upgrade to 1.0.0 version

* Tue Nov 26 2013 Daniel Bruno <dbruno@fedoraproject.org> - 0.4.3-1
- First RPM release

