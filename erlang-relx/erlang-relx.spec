%define bname relx
Name:           erlang-%bname
Version:        3.21.1
Release:        2
Summary:        A release assembler for Erlang
License:        Apache-2.0
Group:          Development/Tools/Other
URL:            https://github.com/erlware/%bname
Source:         %bname-%version.tar.gz

Patch0:         %bname-%version-git.patch
Patch1:         %bname-2.0.0-doc.patch

Provides:       erlang-%bname = %version-%release

BuildRequires:  erlang-rpm-macros
BuildRequires:  erlang
BuildRequires:  erlang-common_test
BuildRequires:  erlang-erlware_commons >= 0.18.0
BuildRequires:  erlang-providers >= 1.6.0
BuildRequires:  erlang-rebar >= 2.6.1

%description
Relx assembles releases for an Erlang/OTP release. Given a release specification
and a list of directories in which to search for OTP applications it will
generate a release output. That output depends heavily on what plugins available
and what options are defined, but usually it is simply a well configured release
directory.
The release-specification-file is optional but otherwise contains additional
specification information for releases.

# avoid error on Fedora 25: error: Empty %files file /home/abuild/rpmbuild/BUILD/erlware_commons/debugfiles.list
%global debug_package %{nil}

%prep
%setup -q -n %bname-%version
%patch0 -p1
%patch1 -p1
sed -i -r '1s|^.*/env[[:blank:]]+(.*)$|#!%_bindir/\1|' priv/templates/install_upgrade_escript
erl -noshell -eval '
A = "src/%bname.app.src",
{ok, [{application, %bname, L}]} = file:consult(A),
file:write_file(A, io_lib:format("{application, %bname, ~p}.~n", [[{vsn, "%version"}|proplists:delete(vsn, L)]])),
halt().'


%build
erl -noshell -eval '
{ok, L} = file:consult("rebar.config"),
file:write_file("%bname.rebar.config",
                lists:map(fun(E) -> [io_lib:print(E), ".\n"] end,
                          [{erl_opts, [slim, inline, no_debug_info, nowarn_deprecated_function|lists:delete(debug_info, proplists:get_value(erl_opts, L, []))]},
                           {eunit_opts, [nowarn_deprecated_function|proplists:get_value(eunit_opts, L, [])]}
                           |lists:foldl(fun proplists:delete/2, L, [deps, erl_opts, eunit_opts, cover_enabled])])),
halt().'
for c in compile doc; do
	rebar -C %bname.rebar.config $c -v
done
cat > %bname.escript <<__EOF__
#!/usr/bin/escript
%%!-noinput
main(X) -> relx:main(X).
__EOF__


%install
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/ebin
install -p -m 0644 ebin/* %buildroot%_otplibdir/%bname-%version/ebin/
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/include
install -p -m 0644 include/* %buildroot%_otplibdir/%bname-%version/include/
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/priv/templates
for i in priv/templates/*; do
	case $i in
		*bin|*script) m="0755" ;;
		*) m="0644" ;;
	esac
	install -p -m $m $i %buildroot%_otplibdir/%bname-%version/priv/templates/
done
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/doc
install -p -m 0644 doc/*.{css,html,png} %buildroot%_otplibdir/%bname-%version/doc/
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/examples
install -p -m 0644 examples/* %buildroot%_otplibdir/%bname-%version/examples/
install -d -m 0755 %buildroot%_docdir/%name
ln -sf %_otplibdir/%bname-%version/doc %buildroot%_docdir/%name/html
install -p -m 0644 README* CONTRIBUTING* %buildroot%_docdir/%name/
install -pD -m 0755 %bname.escript %buildroot%_bindir/%bname


%check
rebar -C %bname.rebar.config eunit


%files
%defattr(-,root,root)
%doc %_docdir/%name
%_otplibdir/*
%_bindir/*


%changelog
* Thu May 25 2017 Timotheus Pokorra <tp@tbits.net> 3.21.1-2
- fix for Fedora 25, there is no debugging information

* Thu Oct 20 2016 Led <ledest@gmail.com> 3.21.1-1
- 3.21.1
- git 53a87ed

* Fri Aug 26 2016 Led <ledest@gmail.com> 3.21.0-1
- 3.21.0

* Mon Jul 25 2016 Led <ledest@gmail.com> 3.20.0-1
- 3.20.0

* Sat Apr 02 2016 Led <ledest@gmail.com> 3.18.0-1
- 3.18.0
- git 1e15397

* Sat Apr 02 2016 Led <ledest@gmail.com> 3.17.0-1
- 3.17.0
- clean up and update BuildRequires

* Sun Feb 14 2016 Led <ledest@gmail.com> 3.15.0-1
- 3.15.0

* Sun Jan 17 2016 Led <ledest@gmail.com> 3.13.0-1
- 3.13.0
- add patches:
  + relx-3.13.0-git.patch

* Sun Nov 29 2015 Led <ledest@gmail.com> 3.9.0-1
- 3.9.0
- remove patches:
  + relx-3.7.1-git.patch

* Sun Oct 11 2015 Led <ledest@gmail.com> 3.7.1-1
- 3.7.1

* Fri Sep 04 2015 Led <ledest@gmail.com> 3.5.0-1
- 3.5.0
- add patches:
  + relx-3.5.0-git.patch

* Sat Jul 04 2015 Led <ledest@gmail.com> 3.1.0-1
- 3.1.0
- fix changelog

* Sat Jul 04 2015 Led <ledest@gmail.com> 2.1.0-1
- 2.1.0

* Thu Jul 02 2015 Led <ledest@gmail.com> 2.0.0-2
- fix build with Erlang 18

* Sun May 31 2015 Led <ledest@gmail.com> 2.0.0-1
- initial build
