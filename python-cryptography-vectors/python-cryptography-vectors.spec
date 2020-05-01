%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2:        %global __python2 /usr/bin/python2}
%{!?python2_sitelib:  %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%global modname cryptography-vectors
%global pymodname cryptography_vectors

Name:               python-%{modname}
Version:            0.6.1
Release:            1.26%{?dist}.kolab_wf
Summary:            Test vectors for the cryptography package

Group:              Development/Libraries
License:            ASL 2.0
URL:                http://pypi.python.org/pypi/cryptography-vectors
Source0:            https://pypi.python.org/packages/source/c/%{modname}/cryptography_vectors-%{version}.tar.gz

BuildArch:          noarch
BuildRequires:      python2-devel python-setuptools

%description
Test vectors for the cryptography package.

The only purpose of this package is to be a building requirement for
python-cryptography, otherwise it has no use. Don’t install it unless
you really know what you are doing.

%prep
%setup -q -n %{pymodname}-%{version}

# Remove bundled egg-info in case it exists
rm -rf %{modname}.egg-info


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build


%install

%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}

%check
%{__python2} setup.py test || :


%files
%doc LICENSE
%{python2_sitelib}/%{pymodname}/
%{python2_sitelib}/%{pymodname}-%{version}*



%changelog
* Thu Oct 16 2014 Matej Cepl <mcepl@redhat.com> - 0.6.1-1
- New upstream release (fixes among others #1153501)

* Wed Oct 01 2014 Matej Cepl <mcepl@redhat.com> - 0.5.4-3
- Add LICENSE file from the upstream repo.

* Mon Sep 29 2014 Matej Cepl <mcepl@redhat.com> - 0.5.4-2
- initial package for Fedora
