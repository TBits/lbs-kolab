%define bname erlware_commons
Name:           erlang-%bname
Version:        0.21.0
Release:        2%{?dist}
Summary:        An Erlang providers library
License:        Apache-2.0
Group:          Development/Tools/Other
URL:            https://github.com/erlware/%bname
Source:         %bname.tar.xz
Provides:       erlang-%bname = %version-%release

BuildRequires:  erlang-rpm-macros
BuildRequires:  erlang-rebar >= 2.6.1
BuildRequires:  erlang

%description
Providers is an Erlang providers library.

# avoid error on Fedora 25: error: Empty %files file /home/abuild/rpmbuild/BUILD/erlware_commons/debugfiles.list
%global debug_package %{nil}

%prep
%setup -q -n %bname


%build
erl -noshell -eval '
{ok, L} = file:consult("rebar.config"),
file:write_file("%bname.rebar.config",
                lists:map(fun(E) -> io_lib:format("~p.~n", [E]) end,
                          [{erl_opts, [slim, inline, no_debug_info, nowarn_deprecated_function|lists:delete(debug_info, proplists:get_value(erl_opts, L, []))]},
                           {edoc_opts, [{preprocess, true}|proplists:get_value(edoc_opts, L, [])]}
                           |lists:foldl(fun proplists:delete/2, L, [deps, cover_enabled, edoc_opts, erl_opts])])),
halt().'
for c in compile doc; do
	rebar -C %bname.rebar.config $c -v
done


%install
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/ebin
install -p -m 0644 ebin/* %buildroot%_otplibdir/%bname-%version/ebin/
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/include
install -p -m 0644 include/* %buildroot%_otplibdir/%bname-%version/include/
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/priv
install -p -m 0644 priv/* %buildroot%_otplibdir/%bname-%version/priv/
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
* Thu May 25 2017 Timotheus Pokorra <tp@tbits.net> 0.21.0-2
- fix for Fedora 25, there is no debugging information

* Sat Jun 11 2016 Led <ledest@gmail.com> 0.21.0-1
- 0.21.0

* Tue Mar 29 2016 Led <ledest@gmail.com> 0.18.0-0.2
- clean up BuildRequires

* Wed Mar 16 2016 Led <ledest@gmail.com> 0.18.0-0.1
- 0.18.0

* Thu Dec 24 2015 Led <ledest@gmail.com> 0.16.1-1
- 0.16.1

* Sun Sep 27 2015 Led <ledest@gmail.com> 0.15.0-4
- fix build docs on Erlang R15, R16
- disable debug_info
- disable cover
- remove patches:
  + erlware_commons-0.12.0-doc.patch

* Sun Sep 27 2015 Led <ledest@gmail.com> 0.15.0-3
- fix build docs on Erlang R15, R16

* Fri Sep 04 2015 Led <ledest@gmail.com> 0.15.0-2
- disable git tests
- clean ups

* Fri Sep 04 2015 Led <ledest@gmail.com> 0.15.0-1
- 0.15.0

* Sat Jul 04 2015 Led <ledest@gmail.com> 0.13.0-1
- 0.13.0
- remove patches:
  + erlware_commons-0.12.0-git.patch

* Tue Jun 02 2015 Led <ledest@gmail.com> 0.12.0-2
- add patches:
  + erlware_commons-0.12.0-git.patch

* Sun May 31 2015 Led <ledest@gmail.com> 0.12.0-1
- initial build
