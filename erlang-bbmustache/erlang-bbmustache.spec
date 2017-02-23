%define bname bbmustache
Name:           erlang-%bname
Version:        1.3.0
Release:        1%{?dist}
Summary:        Binary pattern match Based Mustache template engine for Erlang/OTP
License:        MIT
Group:          Development/Tools/Other
URL:            https://github.com/soranoba/%bname
Source:         %bname-%version.tar.xz
Provides:       erlang-%bname = %version-%release

BuildRequires:  erlang-rpm-macros
BuildRequires:  erlang-rebar
BuildRequires:  erlang-erl_interface
BuildRequires:  erlang-eunit_formatters

%description
%summary.


%prep
%setup -q -n %bname-%version


%build
erl -noshell -eval '
{ok, L} = file:consult("rebar.config"),
file:write_file("%bname.rebar.config",
                lists:map(fun(E) -> [io_lib:print(E), ".\n"] end,
                          [{erl_opts, [slim, inline, no_debug_info|lists:delete(debug_info, proplists:get_value(erl_opts, L, []))]}|lists:foldl(fun proplists:delete/2, L, [deps, erl_opts, cover_enabled])])),
halt().'
rebar -C %bname.rebar.config compile -v


%install
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/ebin
install -p -m 0644 ebin/* %buildroot%_otplibdir/%bname-%version/ebin/


%check
rebar -C %bname.rebar.config eunit


%files
%defattr(-,root,root)
%doc README*
%_otplibdir/*


%changelog
* Mon Sep 19 2016 Led <ledest@gmail.com> 1.3.0-1
- 1.3.0

* Mon Aug 29 2016 Led <ledest@gmail.com> 1.2.0-1
- 1.2.0

* Sun Feb 14 2016 Led <ledest@gmail.com> 1.1.0-1
- 1.1.0

* Sun Jan 17 2016 Led <ledest@gmail.com> 1.0.5-1
- 1.0.5

* Sat Jul 04 2015 Led <ledest@gmail.com> 1.0.3-1
- initial build
