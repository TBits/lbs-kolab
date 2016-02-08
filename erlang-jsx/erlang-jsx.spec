
%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global installdir %{_libdir}/erlang/lib/jsx-%{version}
%global debug_package %{nil}

Name:          erlang-jsx
Version:       2.4.0
Release:       1%{?dist}
Summary:       A streaming, evented json parsing toolkit
License:       MIT
URL:           https://github.com/talentdeficit/jsx
Source0:       https://github.com/talentdeficit/jsx/archive/jsx-%{version}.tar.gz

BuildRequires: erlang-rebar
Requires:      erlang-erts%{?_isa} >= R14B
Requires:      erlang-stdlib%{?_isa}

%description
An erlang application for consuming, producing and
manipulating json. inspired by yajl.

%prep
%setup -q -n jsx-%{version}

%build
rebar compile -v

%install
mkdir -p \
    %{buildroot}%{installdir}/ebin \
    %{buildroot}%{installdir}/.eunit

install -pm 644 ebin/jsx.app %{buildroot}%{installdir}/ebin
install -pm 644 rebar.config %{buildroot}%{installdir}/
install -pm 644 ebin/*.beam %{buildroot}%{installdir}/ebin

%check
rebar eunit -v

%files
%{installdir}
%doc CHANGES.md LICENSE README.md

%changelog
* Fri May 15 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.0-1
- Check in 2.4.0

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 01 2013 gil cattaneo <puntogil@libero.it> 1.4.2-2
- add debug_package nil
- fix requires list
- drop erlang-eunit

* Fri Jul 12 2013 gil cattaneo <puntogil@libero.it> 1.4.2-1
- initial rpm
