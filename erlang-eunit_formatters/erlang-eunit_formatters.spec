%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%global realname eunit_formatters
%global upstream seancribbs
%global debug_package %{nil}
%global git_tag 96b6ced
%global patchnumber 0


Name:		erlang-%{realname}
Version:	0.1.2
Release:	1%{?dist}
Summary:	Because eunit's output sucks
Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/basho/riak_dt
# wget --content-disposition https://github.com/seancribbs/eunit_formatters/tarball/0.1.2
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz

# Compile-time requirements
BuildRequires:	erlang-rebar

Requires:	erlang-kernel%{?_isa}
Requires:	erlang-stdlib%{?_isa} >= R13B

%description
Because eunit's output sucks. Let's make it better.


%prep
%setup -q -n %{upstream}-%{realname}-%{git_tag}
sed -i -e "s,git,\"%{version}\",g" src/%{realname}.app.src

%build
rebar compile -v


%install
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,priv}
install -p -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin


%check
rebar eunit skip_deps=true -v || :


%files
%doc README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/*.beam


%changelog
* Thu Jul  9 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.1.2-1
- Initial package
