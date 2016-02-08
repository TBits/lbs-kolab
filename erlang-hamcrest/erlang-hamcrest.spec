
%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname hamcrest
%global upstream hyperthunk
# Techincally, we're noarch; but erlang whose directories we install into is not.
%global debug_package %{nil}
%global git_tag 01e21ec
%global patchnumber 0


Name:           erlang-%{realname}
Version:        0.1.0
Release:        1%{?dist}
Summary:        Hamcrest for Erlang
Group:          Development/Libraries
License:        ASL 2.0
URL:            http://hyperthunk.github.com/hamcrest-erlang/
# wget --content-disposition https://github.com/hyperthunk/hamcrest-erlang/tarball/0.1.0
Source0:	    %{upstream}-%{realname}-erlang-%{version}-%{patchnumber}-g%{git_tag}.tar.gz

Patch1:         relax-proper-dep.patch

BuildRequires:  erlang-rebar
BuildRequires:  erlang-proper

Requires:       erlang-compiler%{?_isa}
Requires:       erlang-erts%{?_isa}
Requires:       erlang-kernel%{?_isa}
Requires:       erlang-stdlib%{?_isa}
# Error:erlang(cover:compile_beam/2)
# Error:erlang(cover:get_term/1)
# Error:erlang(cover:write/2)
Requires:       erlang-tools%{?_isa}

%description
With %{realname} you can easily mock modules in Erlang. Since %{realname} is intended to be
used in testing, you can also perform some basic validations on the mocked
modules, such as making sure no function is called in a way it should not.

%prep
%setup -q -n %{upstream}-%{realname}-erlang-4002aa0

%patch1 -p1

%build
rebar compile -v

%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include
install -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 include/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include

%check
# There's no testing this crap
exit 0
mkdir -p test/hamcrest
ln -s ../../include test/hamcrest
rebar skip_deps=true eunit -v

%files
%doc LICENCE README.markdown NOTES TODO.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/*.hrl

%changelog
* Fri May 15 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.1.0-1
- First package
