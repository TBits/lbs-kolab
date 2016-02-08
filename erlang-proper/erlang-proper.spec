
%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname proper
%global upstream manopapad
# Techincally, we're noarch; but erlang whose directories we install into is not.
%global debug_package %{nil}
%global git_tag 87e4a56
%global patchnumber 0


Name:           erlang-%{realname}
Version:        1.1
Release:        1%{?dist}
Summary:        Property based test tooling for Erlang
Group:          Development/Libraries
License:        GPLv3+
URL:            http://manopapad.github.com/proper/
# wget --content-disposition https://github.com/manopapad/proper/tarball/v1.1
Source0:        %{upstream}-%{realname}-v%{version}-%{patchnumber}-g%{git_tag}.tar.gz

BuildRequires:  erlang-rebar

Requires:       erlang-compiler%{?_isa}
Requires:       erlang-erts%{?_isa}
Requires:       erlang-kernel%{?_isa}
Requires:       erlang-stdlib%{?_isa}
# Error:erlang(cover:compile_beam/2)
# Error:erlang(cover:get_term/1)
# Error:erlang(cover:write/2)
Requires:       erlang-tools%{?_isa}


%description
PropEr (PROPerty-based testing tool for ERlang) is a QuickCheck-
inspired open-source property-based testing tool for Erlang, developed
by Manolis Papadakis, Eirini Arvaniti and Kostis Sagonas.

The base PropEr system was written mainly by Manolis Papadakis, and
the stateful code testing subsystem by Eirini Arvaniti.

%prep
%setup -q -n %{upstream}-%{realname}-%{git_tag}


%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include
install -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 include/*.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include
install -m 644 rebar.config %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/


%check
mkdir -p test/proper
ln -s ../../include test/proper/include
rm -rf test/rec_props_test1.erl
rm -rf test/rec_props_test2.erl
sed -i \
    -e '/rec_props_test1/d' \
    -e '/rec_props_test2/d' \
    test/proper_tests.erl
rebar eunit -v


%files
%doc COPYING README.md THANKS
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/proper.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/*.hrl
%{_libdir}/erlang/lib/%{realname}-%{version}/rebar.config

%changelog
* Fri May 15 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.1.0-1
- First package
