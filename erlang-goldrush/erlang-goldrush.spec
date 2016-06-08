%global realname goldrush
%global upstream DeadZen
# Technically, we're noarch; but erlang whose directories we install into is not.
%global debug_package %{nil}


Name:       erlang-%{realname}
Version:    0.1.8
Release:    3%{?dist}

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
%{rebar_compile}
%{rebar_doc}


%install
mkdir -p %{buildroot}%{_erllibdir}/%{realname}-%{version}/ebin
install -p -m 644 ebin/%{realname}.app ebin/*.beam %{buildroot}%{_erllibdir}/%{realname}-%{version}/ebin


%check
%{rebar_eunit}


%files
%license LICENSE
%doc README.org
%{_erllibdir}/%{realname}-%{version}


%changelog
* Mon Mar  7 2016 Peter Lemenkov <lemenkov@gmail.com> - 0.1.8-3
- Spec-file cleanups

* Fri Mar  4 2016 Peter Lemenkov <lemenkov@gmail.com> - 0.1.8-2
- Build with autodeps

* Thu Feb 18 2016 Randy Barlow <rbarlow@redhat.com> - 0.1.8-1
- Initial release.
