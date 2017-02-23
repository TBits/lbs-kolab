%global elixir_version %(%{_bindir}/elixir -v | grep ^Elixir | awk '{print $2}')

%global debug_package %nil

%global _elixir_mix_libdir %{_datadir}/elixir/%{elixir_version}/lib/mix

Name:           hex
Version:        0.13.1
Release:        1%{?dist}
Summary:        Hex for Elixir and Erlang

Group:          Applications/Web
License:        MIT
URL:            http://hexpm.org
#Source0:        https://github.com/hexpm/hex/archive/v0.13.1.tar.gz
Source0:        hex-0.13.1.tar.gz

BuildRequires:  elixir
Requires:       elixir

%description
Hex, for Elixir and Erlang

%prep
%setup -q

%build
MIX_ENV=prod mix archive.build

%install
find -type f

mkdir -p \
    %{buildroot}%{_elixir_mix_libdir}/lib/hex/ebin/

cp -av _build/prod/lib/hex/ebin/* \
    %{buildroot}%{_elixir_mix_libdir}/lib/hex/ebin/.

%files
%dir %{_elixir_mix_libdir}/lib/
%dir %{_elixir_mix_libdir}/lib/hex/
%dir %{_elixir_mix_libdir}/lib/hex/ebin/
%{_elixir_mix_libdir}/lib/hex/ebin/*.beam
%{_elixir_mix_libdir}/lib/hex/ebin/*.app


%changelog
* Mon Sep 19 2016 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.13.1-1
- Check in 0.13.1

* Sun Jun  5 2016 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.12.1-1
- First package
