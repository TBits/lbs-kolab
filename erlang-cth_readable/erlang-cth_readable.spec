%global realname cth_readable
%global upstream ferd

# Technically we're noarch, but our install path is not.
%global debug_package %{nil}

Name:     erlang-%{realname}
Version:  1.2.3
Release:  1%{?dist}
Summary:  Common test hooks for more readable erlang logs
License:  BSD
URL:      https://github.com/%{upstream}/%{realname}
Source0:  https://github.com/%{upstream}/%{realname}/archive/v%{version}/%{realname}-%{version}.tar.gz
BuildRequires:  erlang-cf
BuildRequires:  erlang-rebar
Requires:       erlang-rebar

%description
%{summary}.

%prep
%autosetup -n %{realname}-%{version}

%build
%{erlang_compile}

%install
%{erlang_install}

%check
%{erlang_test}

%files
%license LICENSE
%doc README.md
%{erlang_appdir}/

%changelog
* Sat Jul 14 2018 Timothée Floure <fnux@fedoraproject.org> - 1.4.2-1
- Let there be package
