
%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname inert
%global upstream msantos
%global debug_package %{nil}
%global git_tag 591b45d
%global patchnumber 0

Name:           erlang-%{realname}
Version:        0.6.1
Release:        1%{?dist}
Summary:        Asynchronous notification of events on file descriptors
Group:          Development/Languages
License:        Public Domain or ASL 2.0
URL:            https://github.com/msantos/inert
# wget --content-disposition https://github.com/msantos/inert/tarball/0.6.1
Source0:        %{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  erlang-rebar
# Error:erlang(os:timestamp/0) - in R12B
Requires:       erlang-erts%{?_isa} >= R13B
# Error:erlang(queue:member/2 - in R12B
Requires:       erlang-stdlib%{?_isa} >= R13B

%description
inert is a library for asynchronous notification of events on file
descriptors.

To be scheduler friendly, inert uses the native Erlang socket polling
mechanism.

%prep
%setup -q -n %{upstream}-%{realname}-%{git_tag}

%build
rebar compile -v

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
install -p -m 0644 -D ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -p -m 0644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin


%clean
rm -rf %{buildroot}


%check
#rebar eunit -v


%files
%doc README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam


%changelog
* Fri May 15 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.6.1-1
- First package
