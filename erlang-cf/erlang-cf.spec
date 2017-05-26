%define bname cf
Name:           erlang-%bname
Version:        0.2.2
Release:        2
Summary:        Colored output for Erlang/OTP io and io_lib
License:        MIT
Group:          Development/Tools/Other
URL:            https://github.com/project-fifo/%bname

# wget --content-disposition https://github.com/project-fifo/cf/archive/0.2.2.tar.gz
Source:         cf-0.2.2.tar.gz

Provides:       erlang-%bname = %version-%release

BuildRequires:  rpm-macros-erlang rpm-build-erlang
BuildRequires:  erlang-rebar >= 2.6.1

%description
cf is a helper library for termial colour printing extending the Erlang/OTP
io:format syntax to add colours.

# avoid error on Fedora 25: error: Empty %files file /home/abuild/rpmbuild/BUILD/erlware_commons/debugfiles.list
%global debug_package %{nil}

%prep
%setup -q -n %bname-%version
sed -i \
	-e "/^%%%%/s/\`/'/g" \
	-e '/^%%%%/s/</\&lt;/g' \
	-e '/^%%%%/s/>/\&gt;/g' \
	src/%bname.erl


%build
erl -noshell -eval '
{ok, L} = file:consult("rebar.config"),
file:write_file("%bname.rebar.config",
                lists:map(fun(E) -> io_lib:format("~p.~n", [E]) end,
                          [{erl_opts, [slim, inline, no_debug_info|proplists:delete(debug_info, proplists:get_value(erl_opts, L, []))]},
                           {edoc_opts, [{preprocess, true}|proplists:get_value(edoc_opts, L, [])]}
                           |lists:foldl(fun proplists:delete/2, L, [deps, edoc_opts, erl_opts])])),
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
* Thu May 25 2017 Timotheus Pokorra <tp@tbits.net> 0.2.2-2
- fix for Fedora 25, there is no debugging information

* Sun Nov  6 2016 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> 0.2.2-1
- Update to 0.2.2

* Tue Mar 29 2016 Led <ledest@gmail.com> 0.2.0-2
- clean up BuildRequires

* Thu Dec 24 2015 Led <ledest@gmail.com> 0.2.0-1
- initial build
