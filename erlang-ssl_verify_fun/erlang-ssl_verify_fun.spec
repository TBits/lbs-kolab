%define bname ssl_verify_fun
Name:           erlang-%bname
Version:        1.1.1
Release:        2
Summary:        SSL verification for Erlang
License:        MIT
Group:          Development/Tools/Other
URL:            https://github.com/deadtrickster/%bname.erl
Source:         %bname.erl-%version.tar.gz

BuildRequires:  erlang-rpm-macros
BuildRequires:  erlang-rebar
BuildRequires:  erlang-erl_interface erlang-public_key

%description
SSL verification for Erlang.

# avoid error on Fedora 25: error: Empty %files file /home/abuild/rpmbuild/BUILD/erlware_commons/debugfiles.list
%global debug_package %{nil}

%prep
%setup -q -n %bname.erl-%version

%build
rebar compile -vv
rebar doc -vv

%install
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/ebin
install -p -m 0644 ebin/* %buildroot%_otplibdir/%bname-%version/ebin/
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/doc
install -p -m 0644 doc/*.{css,html,png} %buildroot%_otplibdir/%bname-%version/doc/
install -d -m 0755 %buildroot%_docdir/%name
ln -sf %_otplibdir/%bname-%version/doc %buildroot%_docdir/%name/html
install -p -m 0644 *.md %buildroot%_docdir/%name/

%check
rebar eunit -vv || :

%files
%defattr(-,root,root)
%doc %_docdir/%name
%_otplibdir/*

%changelog
* Thu May 25 2017 Timotheus Pokorra <tp@tbits.net> 1.1.1-2
- fix for Fedora 25, there is no debugging information

* Sun Nov  6 2016 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> 1.1.1-1
- Initial package
