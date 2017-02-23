%global elixir_version %(%{_bindir}/elixir -v | grep ^Elixir | awk '{print $2}')

%global debug_package %nil

%global _elixir_mix_libdir %{_datadir}/elixir/%{elixir_version}/lib/mix

Name:           phoenix
Version:        1.2.1
Release:        1%{?dist}
Summary:        Phoenix Framework

Group:          Applications/Web
License:        MIT
URL:            http://phoenixframework.org
#Source0:        https://github.com/phoenixframework/phoenix/archive/v%{version}.tar.gz
Source0:        phoenix-%{version}.tar.gz

BuildRequires:  elixir
Requires:       elixir

%description
Phoenix Framework

%prep
%setup -q

%build
pushd installer
mix archive.build
popd

%install
find installer -type f

mkdir -p \
    %{buildroot}%{_elixir_mix_libdir}/lib/phoenix/ebin/

cp -av installer/_build/dev/lib/phoenix_new/ebin/* \
    %{buildroot}%{_elixir_mix_libdir}/lib/phoenix/ebin/.

%check
pushd installer
mix test
popd

%files
%doc
%{_elixir_mix_libdir}/lib/phoenix/ebin/*

%changelog
* Mon Sep 19 2016 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.2.1-1
- Check in 1.2.1

* Sun Jun  5 2016 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.1.6-1
- First package
