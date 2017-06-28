%define bname ssl_verify_hostname
Name: erlang-%bname
Version: 1.1.1
Release: 1
Summary: Hostname verification library for Erlang
License: MIT
Group: Development/Tools/Other
URL: https://github.com/deadtrickster/%bname.erl
Source: %bname.erl-%version.tar.gz
Patch1: update-to-and-fix-recent-rebar3-version.patch
BuildArch: noarch
Provides: %bname.erl = %version-%release

BuildRequires:  rpm-macros-erlang rpm-build-erlang
BuildRequires:  erlang-rebar
BuildRequires:  erlang-erl_interface erlang-public_key

%description
Hostname verification library for Erlang.


%prep
%setup -q -n %bname.erl-%version
%patch1 -p1 -R


%build
erl -noshell -eval '
{ok, L} = file:consult("rebar.config"),
file:write_file("%bname.rebar.config",
                lists:map(fun(E) -> io_lib:format("~p.~n", [E]) end,
                          [{erl_opts, [slim,inline,no_debug_info|lists:delete(debug_info, proplists:get_value(erl_opts, L, []))]}
                           |lists:foldl(fun(O, A) -> proplists:delete(O, A) end, L, [deps, erl_opts, cover_enabled])])),
halt().'
for c in compile doc; do
	rebar -C %bname.rebar.config $c -v
done


%install
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/ebin
install -p -m 0644 ebin/* %buildroot%_otplibdir/%bname-%version/ebin/
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/doc
install -p -m 0644 doc/*.{css,html,png} %buildroot%_otplibdir/%bname-%version/doc/
install -d -m 0755 %buildroot%_docdir/%name
ln -sf %_otplibdir/%bname-%version/doc %buildroot%_docdir/%name/html
install -p -m 0644 *.md %buildroot%_docdir/%name/


%check
rebar -C %bname.rebar.config eunit


%files
%defattr(-,root,root)
%doc %_docdir/%name
%_otplibdir/*


%changelog
* Sun Jul 24 2016 Led <ledest@gmail.com> 1.1.1-1
- 1.1.1
- add patches:
  + update-to-and-fix-recent-rebar3-version.patch

* Sun Jul 24 2016 Led <ledest@gmail.com> 1.1.0-1
- 1.1.0

* Sun Jul 24 2016 Led <ledest@gmail.com> 1.0.9-1
- 1.0.9

* Sun Jul 24 2016 Led <ledest@gmail.com> 1.0.8-1
- 1.0.8

* Sun Jan 17 2016 Led <ledest@gmail.com> 1.0.6-1
- initial build
