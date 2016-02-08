%global debug_package %{nil}
%global git_short_hash 6a9845f
%global short_name erlydtl
%global github_username evanmiller


Name:           erlang-%{short_name}
Version:        0.7.0
Release:        5.20130214git%{git_short_hash}%{?dist}
Summary:        Erlang implementation of the Django Template Language
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{github_username}/%{short_name}
# The tarball comes from here:
# http://github.com/%{github_username}/%{short_name}/tarball/master
# GitHub has layers of redirection and renames that make this a troublesome
# URL to include directly.
Source0:        %{github_username}-%{short_name}-%{git_short_hash}.tar.gz
Patch1:         erlang-erlydtl-0001-Remove-support-for-parametrized-modules.patch
Provides:       ErlyDTL = %{version}-%{release}
BuildRequires:  erlang-rebar
Requires:       erlang-compiler%{?_isa}
Requires:       erlang-erts%{?_isa}
Requires:       erlang-eunit%{?_isa}
# FIXME
# Error:erlang(gettext_compile:close_file/0)
# Error:erlang(gettext_compile:fmt_fileinfo/1)
# Error:erlang(gettext_compile:open_po_file/3)
# Error:erlang(gettext_compile:write_header/0)
# Error:erlang(gettext_compile:write_pretty/1)
Requires:       erlang-gettext%{?_isa}
Requires:       erlang-kernel%{?_isa}
Requires:       erlang-stdlib%{?_isa}
Requires:       erlang-syntax_tools%{?_isa}


%description
ErlyDTL is an Erlang implementation of the Django Template Language. The
erlydtl module compiles Django Template source code into Erlang bytecode. The
compiled template has a "render" function that takes a list of variables and
returns a fully rendered document.


%prep
%setup -q -n %{github_username}-%{short_name}-%{git_short_hash}
%patch1 -p1 -b .no_parametrized_modules


%build
rebar compile -v


%check
make test


%install
mkdir -p %{buildroot}/%{_libdir}/erlang/lib/erlydtl-%{version}/
cp -r ebin     %{buildroot}/%{_libdir}/erlang/lib/erlydtl-%{version}/
cp -r bin      %{buildroot}/%{_libdir}/erlang/lib/erlydtl-%{version}/
cp -r priv     %{buildroot}/%{_libdir}/erlang/lib/erlydtl-%{version}/


%files
%dir %{_libdir}/erlang/lib/erlydtl-%{version}
%{_libdir}/erlang/lib/erlydtl-%{version}/*
%doc README_I18N
%doc README.markdown


%changelog
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-5.20130214git6a9845f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-4.20130214git6a9845f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jun 01 2014 Peter Lemenkov <lemenkov@gmail.com> - 0.7.0-3.20130214git6a9845f
- Rebuilt (fix FTBFS, see rhbz #992220)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-2.20130214git6a9845f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 12 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.7.0-1.20130214git6a9845f
- Latest snapshot
- Removed tests for parametrized modules support

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-6.20110306git889155f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-5.20110306git889155f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-4.20110306git889155f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Mar 06 2011 Ilia Cheishvili <ilia.cheishvili@gmail.com> - 0.6.0-3.20110306git889155f
- Update to latest git snapshot

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Aug 1 2010 Ilia Cheishvili <ilia.cheishvili@gmail.com> - 0.6.0-1
- Initial Package
