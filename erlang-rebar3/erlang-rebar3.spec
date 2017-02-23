%global certifi_version %(rpm -q --queryformat='%{VERSION}' erlang-certifi)
%global cf_version %(rpm -q --queryformat='%{VERSION}' erlang-cf)

Name:           erlang-rebar3
Version:        3.3.2
Release:        1%{?dist}
Summary:        A sophisticated build-tool for Erlang projects that follows OTP principles
License:        Apache-2.0
Group:          Development/Tools/Other
URL:            https://github.com/rebar/rebar3
# wget --content-disposition
Source:         https://github.com/erlang/rebar3/archive/rebar3-%{version}/rebar3-%{version}.tar.gz

Patch1:         rebar3-3.1.0-doc.patch

BuildArch:      noarch
Requires:       erlang
Conflicts:      erlang-rebar

BuildRequires:  erlang-rpm-macros
BuildRequires:  erlang-rebar >= 2.6.1
BuildRequires:  erlang-erlware_commons >= 0.18.0
BuildRequires:  erlang-bbmustache >= 1.0.4
BuildRequires:  erlang-certifi >= 0.4.0
BuildRequires:  erlang-providers >= 1.6.0
BuildRequires:  erlang-relx >= 3.17.0
BuildRequires:  erlang-cf >= 0.2.0
BuildRequires:  erlang-eunit_formatters >= 0.3.1
BuildRequires:  erlang-cth_readable >= 1.2.2
BuildRequires:  erlang-getopt >= 0.8.2
BuildRequires:  erlang-ssl_verify_hostname >= 1.0.5
BuildRequires:  erlang-ssl_verify_fun >= 1.1.1
BuildRequires:  erlang-public_key

%description
Rebar3 is an Erlang build tool that makes it easy to compile and test Erlang
applications, port drivers and releases. rebar3 is a self-contained Erlang
script, so it's easy to distribute or even embed directly in a project. Where
possible, rebar3 uses standard Erlang/OTP conventions for project structures,
thus minimizing the amount of build configuration work. rebar3 also provides
dependency management, enabling application writers to easily re-use common
libraries from a variety of locations (git, hg, etc).

%prep
%setup -q -n rebar3-%version
%patch1 -p1
sed -i 's/ @\(equiv \)/ \1/g' src/rebar_erlc_compiler.erl

sed -i -r \
    -e 's/certifi,(\s+)".*"/certifi,\1"%{certifi_version}"/g' \
    -e 's/cf,(\s+)".*"/cf,\1"%{cf_version}"/g' \
    rebar.config

%build
rebar compile -v
rebar doc -v
cat >> rebar3.escript << EOF
#!/usr/bin/env escript
%%! -noshell -noinput

main (Args) ->
    rebar3:main(Args).
EOF

%install
find | sort
install -pD -m 0755 rebar3.escript %buildroot%_bindir/rebar3
for d in ebin priv/templates; do
	install -d -m 0755 %buildroot%_otplibdir/rebar-%version/$d
	install -p -m 0644 $d/* %buildroot%_otplibdir/rebar-%version/$d/
done
install -d -m 0755 %buildroot%_otplibdir/rebar-%version/doc
install -p -m 0644 doc/*.{css,html,png} %buildroot%_otplibdir/rebar-%version/doc/
install -d -m 0755 %buildroot%_docdir/%name
ln -sf %_otplibdir/rebar-%version/doc %buildroot%_docdir/%name/html
install -p -m 0644 CONTRIBUTING* README* THANKS* %buildroot%_docdir/%name/

%add_erlang_req_app_skiplist relx

%if 0
%check
./rebar3 ct
%endif


%files
%defattr(-,root,root)
%doc %_docdir/%name
%_otplibdir/*
%_bindir/rebar3

%changelog
* Sun Oct 30 2016 Led <ledest@gmail.com> 3.3.2-1
- 3.3.2

* Mon Sep 12 2016 Led <ledest@gmail.com> 3.3.1-1
- 3.3.1

* Fri Aug 12 2016 Led <ledest@gmail.com> 3.2.0-1
- 3.2.0

* Fri Jul 15 2016 Led <ledest@gmail.com> 3.1.0-3
- fix BuildRequires

* Sun Apr 10 2016 Led <ledest@gmail.com> 3.1.0-2
- add conflicts to rebar

* Sun Apr 10 2016 Led <ledest@gmail.com> 3.1.0-1
- initial build
