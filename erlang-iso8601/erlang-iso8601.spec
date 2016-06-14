
%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname iso8601
%global upstream aseigo
%global debug_package %{nil}
%global git_tag 4530fa0
%global patchnumber 0

Name:           erlang-%{realname}
Version:        1.2
Release:        0.1.git%{?dist}
Summary:        Formats and parses ISO 8601 dates
Group:          Development/Languages
License:        Public Domain or ASL 2.0
URL:            https://github.com/aseigo/erlang_iso8601
# wget --content-disposition https://github.com/aseigo/erlang_iso8601/tarball/master
Source0:        %{upstream}-erlang_%{realname}-%{git_tag}.tar.gz

Patch0001:      0001-Erlang-R18-compatibility.patch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  erlang-rebar
# Error:erlang(os:timestamp/0) - in R12B
Requires:       erlang-erts%{?_isa} >= R13B
# Error:erlang(queue:member/2 - in R12B
Requires:       erlang-stdlib%{?_isa} >= R13B

%description
Formats and parses ISO 8601 dates

%prep
%setup -q -n %{upstream}-erlang_%{realname}-%{git_tag}

%patch0001 -p1

%build
rebar compile -v

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
install -p -m 0644 -D ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -p -m 0644 ebin/%{realname}.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin

%clean
rm -rf %{buildroot}

%check
rebar eunit -v

%files
%doc LICENSE README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/.eunit
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam


%changelog
* Fri May 15 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.6.1-1
- First package
