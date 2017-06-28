%define bname certifi
Name: erlang-%bname
Version: 0.7.0
Release: 2%{?dist}
Summary: An Erlang specific port of certifi
License: MIT
Group: Development/Tools/Other
URL: https://github.com/certifi/%name
Source: %name-%version.tar.gz

BuildRequires: erlang-rpm-macros
BuildRequires: erlang-rebar >= 2.6.1

%description
This Erlang library contains a CA bundle that you can reference in your Erlang
application. This is useful for systems that do not have CA bundles that Erlang
can find itself, or where a uniform set of CAs is valuable.
This an Erlang specific port of certifi (http://certifi.io/). The CA bundle is
derived from Mozilla's canonical set.

# avoid error on Fedora 25: error: Empty %files file /home/abuild/rpmbuild/BUILD/erlware_commons/debugfiles.list
%global debug_package %{nil}

%prep
%setup -q


%build
erl -noshell -eval '
{ok, L} = file:consult("rebar.config"),
file:write_file("%bname.rebar.config",
                lists:map(fun(E) -> [io_lib:print(E), ".\n"] end,
                          [{erl_opts, [slim, inline, no_debug_info|lists:delete(debug_info, proplists:get_value(erl_opts, L, []))]}
                           |lists:foldl(fun proplists:delete/2, L, [deps, erl_opts])])),
halt().'
for c in compile doc; do
	rebar -C %bname.rebar.config $c -v
done


%install
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/ebin
install -p -m 0644 ebin/* %buildroot%_otplibdir/%bname-%version/ebin/
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/priv
install -p -m 0644 priv/* %buildroot%_otplibdir/%bname-%version/priv/
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/doc
install -p -m 0644 doc/*.{css,html,png} %buildroot%_otplibdir/%bname-%version/doc/
install -d -m 0755 %buildroot%_docdir/%name
ln -sf %_otplibdir/%bname-%version/doc %buildroot%_docdir/%name/html
install -p -m 0644 *.md %buildroot%_docdir/%name/


%files
%defattr(-,root,root)
%doc %_docdir/%name
%_otplibdir/*


%changelog
* Thu May 25 2017 Timotheus Pokorra <tp@tbits.net> 0.7.0-2
- fix for Fedora 25, there is no debugging information

* Mon Oct 10 2016 Led <ledest@gmail.com> 0.7.0-1
- 0.7.0

* Mon Aug 29 2016 Led <ledest@gmail.com> 0.5.0-1
- 0.5.0

* Sun Apr 10 2016 Led <ledest@gmail.com> 0.4.0-1
- 0.4.0

* Sun Jan 17 2016 Led <ledest@gmail.com> 0.3.0-1
- initial build
