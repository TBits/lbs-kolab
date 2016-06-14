%global realname proper
%global upstream manopapad
# Technically, we're noarch; but erlang whose directories we install into is not.
%global debug_package %{nil}
%global commit 1b773eeb47cb2c3116d78bdf681505703b762eee


Name:       erlang-%{realname}
Version:    1.1
Release:    6%{?dist}
Summary:    A QuickCheck-inspired property-based testing tool for Erlang

License:    GPLv3+
URL:		https://github.com/%{upstream}/%{realname}
%if 0%{?el7}%{?fedora}
VCS:		scm:git:https://github.com/%{upstream}/%{realname}.git
%endif
#Source0:	https://github.com/%{upstream}/%{realname}/archive/v%{version}/%{realname}-%{version}.tar.gz
# For now we are packaging a commit, because the 1.1 release does not build on Erlang 18 and
# upstream has not made a release since 2013.
Source0:    https://github.com/manopapad/proper/archive/%{commit}.tar.gz

BuildRequires: erlang-rebar


%description
PropEr (PROPerty-based testing tool for ERlang) is a QuickCheck-inspired
open-source property-based testing tool for Erlang.


%prep
%setup -n %{realname}-%{commit}


%build
%rebar_compile
./make_doc


%install
mkdir -p %{buildroot}%{_erllibdir}/%{realname}-%{version}/{ebin,include}
install -pm 644 ebin/* %{buildroot}%{_erllibdir}/%{realname}-%{version}/ebin
install -pm644 include/proper* %{buildroot}%{_erllibdir}/%{realname}-%{version}/include


%files
%if 0%{?fedora}
%license COPYING
%else
%doc COPYING
%endif
%doc doc
%doc examples
%doc README.md
%{_erllibdir}/%{realname}-%{version}/


%changelog
* Sat Mar  5 2016 Peter Lemenkov <lemenkov@gmail.com> - 1.1-6
- Build with autodeps

* Sun Feb 21 2016 Randy Barlow <rbarlow@redhat.com> 1.1-5
- Package commit 1b773eeb (current master) because 1.1 FTBFS (#1307470).
- The unit tests do not pass on current master, so they are disabled.
- Use the autosetup macro.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 09 2016 Randy Barlow <rbarlow@redhat.com> - 1.1-3
- Use the erllibdir macro.

* Thu Jan 07 2016 Randy Barlow <rbarlow@redhat.com> - 1.1-2
- Correct the license from GPLv3 to GPLv3+.

* Tue Jan 05 2016 Randy Barlow <rbarlow@redhat.com> - 1.1-1
- Initial release.
