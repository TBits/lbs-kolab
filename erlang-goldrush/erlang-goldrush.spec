%global realname goldrush
%global upstream DeadZen
# Technically, we're noarch; but erlang whose directories we install into is not.
%global debug_package %{nil}


Name:       erlang-%{realname}
Version:    0.2.0
Release:    2%{?dist}

Summary:    Small, fast event processing and monitoring for Erlang/OTP applications
License:    MIT
URL:		https://github.com/%{upstream}/%{realname}
%if 0%{?el7}%{?fedora}
VCS:		scm:git:https://github.com/%{upstream}/%{realname}.git
%endif
Source0:	https://github.com/%{upstream}/%{realname}/archive/%{version}/%{realname}-%{version}.tar.gz
BuildRequires:	erlang-rebar


%description
A small Erlang app that provides fast event stream processing.


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
%doc README.org
%{erlang_appdir}/


%changelog
* Wed Jul 04 2018 Christoph Erhardt <kolab@sicherha.de> - 0.2.0-2
- Revert conversion to noarch package.

* Sun Jun 17 2018 Randy Barlow <bowlofeggs@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0 (#1588473).
- https://github.com/DeadZen/goldrush/compare/0.1.9...DeadZen:0.2.0
- Convert to a noarch package.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu May 26 2016 Peter Lemenkov <lemenkov@gmail.com> - 0.1.9-1
- Ver. 0.1.9

* Mon Mar  7 2016 Peter Lemenkov <lemenkov@gmail.com> - 0.1.8-3
- Spec-file cleanups

* Fri Mar  4 2016 Peter Lemenkov <lemenkov@gmail.com> - 0.1.8-2
- Build with autodeps

* Thu Feb 18 2016 Randy Barlow <rbarlow@redhat.com> - 0.1.8-1
- Initial release.
