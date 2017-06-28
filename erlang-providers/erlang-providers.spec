%define bname providers
Name:           erlang-%bname
Version:        1.6.0
Release:        3
Summary:        An Erlang providers library
License:        LGPL-3.0
Group:          Development/Tools/Other
URL:            https://github.com/tsloughter/%bname
Source:         %bname-%version.tar.gz
Provides:       erlang-%bname = %version-%release

BuildRequires:  erlang-rpm-macros
BuildRequires:  erlang-rebar
BuildRequires:  erlang-erl_interface
BuildRequires:  erlang-getopt
BuildRequires:  erlang-common_test

%description
Providers is an Erlang providers library.

# avoid error on Fedora 25: error: Empty %files file /home/abuild/rpmbuild/BUILD/erlware_commons/debugfiles.list
%global debug_package %{nil}

%prep
%setup -q -n %bname-%version


%build
erl -noshell -eval '
{ok, L} = file:consult("rebar.config"),
file:write_file("%bname.rebar.config",
                lists:map(fun(E) -> io_lib:format("~p.~n", [E]) end,
                          [{erl_opts, [slim,inline|proplists:delete(debug_info, proplists:get_value(erl_opts, L, []))]}|proplists:delete(deps, proplists:delete(erl_opts, L))])),
halt().'
for c in compile doc; do
	rebar -C %bname.rebar.config $c -v
done


%install
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/ebin
install -p -m 0644 ebin/* %buildroot%_otplibdir/%bname-%version/ebin/
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/include
install -p -m 0644 include/* %buildroot%_otplibdir/%bname-%version/include/
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/doc
install -p -m 0644 doc/*.{css,html,png} %buildroot%_otplibdir/%bname-%version/doc/
install -d -m 0755 %buildroot%_docdir/%name
ln -sf %_otplibdir/%bname-%version/doc %buildroot%_docdir/%name/html
install -p -m 0644 README* %buildroot%_docdir/%name/


%check
rebar -C %bname.rebar.config ct


%files
%defattr(-,root,root)
%doc %_docdir/%name
%_otplibdir/*


%changelog
* Thu May 25 2017 Timotheus Pokorra <tp@tbits.net> 1.6.0-3
- fix for Fedora 25, there is no debugging information

* Sun Jan 31 2016 Led <ledest@gmail.com> 1.6.0-2
- add epmd to BuildRequires

* Mon Nov 30 2015 Led <ledest@gmail.com> 1.6.0-1
- 1.6.0

* Sat Jul 04 2015 Led <ledest@gmail.com> 1.4.1-1
- 1.4.1

* Sun May 31 2015 Led <ledest@gmail.com> 1.3.0-2
- fix URL

* Sat May 30 2015 Led <ledest@gmail.com> 1.3.0-1
- initial build
