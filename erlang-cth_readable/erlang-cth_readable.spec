%define bname cth_readable
Name:           erlang-%bname
Version:        1.2.3
Release:        1
Summary:        An Erlang/OTP library to be used for CT log outputs
License:        MIT
Group:          Development/Tools/Other
URL:            https://github.com/ferd/%bname
Source:         %bname-%version.tar.xz
Provides:       erlang-%bname = %version-%release
BuildArch:      noarch

BuildRequires:  rpm-macros-erlang rpm-build-erlang
BuildRequires:  erlang-rebar >= 2.6.1
BuildRequires:  erlang-common_test

%description
An Erlang/OTP library to be used for CT log outputs you want to be readable
around all that noise they contain.


%prep
%setup -q -n %bname-%version


%build
erl -noshell -eval '
{ok, L} = file:consult("rebar.config"),
file:write_file("%bname.rebar.config",
                lists:map(fun(E) -> io_lib:format("~p.~n", [E]) end,
                          [{erl_opts, [slim, inline, no_debug_info|lists:delete(debug_info, proplists:get_value(erl_opts, L, []))]}|lists:foldl(fun proplists:delete/2, L, [deps, erl_opts])])),
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


%files
%defattr(-,root,root)
%doc %_docdir/%name
%_otplibdir/*


%changelog
* Sun Jun 26 2016 Led <ledest@gmail.com> 1.2.3-1
- 1.2.3

* Sun Apr 10 2016 Led <ledest@gmail.com> 1.2.2-1
- 1.2.2

* Sun Jan 17 2016 Led <ledest@gmail.com> 1.2.0-2
- fix app deps

* Sun Jan 17 2016 Led <ledest@gmail.com> 1.2.0-1
- initial build
