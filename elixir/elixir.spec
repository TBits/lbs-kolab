Name:           elixir
Version:        1.3.3
Release:        1%{?dist}
Summary:        A modern approach to programming for the Erlang VM 

Group:          Development/Languages
# See LEGAL (provided by upstream) for explaination/breakdown.
License:        ASL 2.0 and ERPL
URL:            http://elixir-lang.org/

Source0:        https://github.com/elixir-lang/elixir/archive/v%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  erlang >= R17
BuildRequires:  erlang-rebar
BuildRequires:  git

Requires:       erlang >= R17
Requires:       erlang-erts >= R17
Requires:       erlang-inets
Requires:       rebar

%description
Elixir is a programming language built on top of the Erlang VM.
As Erlang, it is a functional language built to support distributed,
fault-tolerant, non-stop applications with hot code swapping.

%prep
%setup -q
rm rebar
ln -s "$(which rebar)" .
sed -i -e "s/time //g" Makefile
find -name '*.bat' -exec rm \{\} \;

# This contains a failing test. We want `make test` for most tests, but
# this deals with ANSI codes which rpmbuild strips.
rm lib/elixir/test/elixir/io/ansi_test.exs

%build
export LANG="en_US.UTF-8"
make %{?_smp_mflags}

%check
export LANG="en_US.UTF-8"
make test

%install
mkdir -p %{buildroot}/%{_datadir}/%{name}/%{version}
cp -ra bin lib %{buildroot}/%{_datadir}/%{name}/%{version}

mkdir -p %{buildroot}/%{_bindir}
ln -s %{_datadir}/%{name}/%{version}/bin/{elixir,elixirc,iex,mix} %{buildroot}/%{_bindir}/

%files
%doc LICENSE
%{_bindir}/elixir
%{_bindir}/elixirc
%{_bindir}/iex
%{_bindir}/mix
%{_datadir}/%{name}


%changelog
* Mon Sep 19 2016 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.3.3-1
- Check in 1.3.3

* Wed Feb 24 2016 Martin Langhoff <martin@laptop.org> - 1.2.3-1
- New upstream release.

* Mon Feb 8 2016 Martin Langhoff <martin@laptop.org> - 1.2.2-1
- New upstream release.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 29 2015 Ricky Elrod <relrod@redhat.com> - 1.1.1-1
- Latest upstream release.
- Re-enable test suite to see what breaks.

* Tue Jun 30 2015 Jochen Schmitt <Jochen herr-schmitt de> - 1.0.5-1
- New upstream release
- set a UTF-8 locale to build elixir
- Disable test suite

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 13 2015 Jochen Schmitt <Jochen herr-schmitt de> - 1.0.3-1
- New upstream release

* Wed Oct 22 2014 Jochen Schmitt <Jochen herr-schmitt de> - 1.0.2-1
- New upstream release

* Thu Oct  9 2014 Jochen Schmitt <Jochen herr-schmitt de> - 1.0.1-2
- Fix wrong Erlang release specification in the BRs

* Wed Oct 8 2014 Ricky Elrod <relrod@redhat.com> - 1.0.1-1
- Update to upstream 1.0.1.

* Sat Oct  4 2014 Jochen Schmitt <Jochen herr-schmitt de> - 1.0-1
- New upstream release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 12 2014 Ricky Elrod <codeblock@fedoraproject.org> - 0.12.5-1
- Update to upstream 0.12.5.

* Thu Feb 13 2014 Ricky Elrod <codeblock@fedoraproject.org> - 0.12.4-1
- Update to upstream 0.12.4.

* Tue Feb 4 2014 Ricky Elrod <codeblock@fedoraproject.org> - 0.12.3-1
- Update to upstream 0.12.3.

* Sun Jan 19 2014 Ricky Elrod <codeblock@fedoraproject.org> - 0.12.2-2
- Remove patch that is no longer needed.

* Fri Jan 17 2014 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.12.2-1
- Update to upstream 0.12.2.

* Sat Jan 11 2014 Ricky Elrod <codeblock@fedoraproject.org> - 0.12.1-1
- Update to upstream 0.12.1.

* Sun Dec 15 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.12.0-1
- Update to upstream 0.12.0.

* Sun Nov 24 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.11.2-1
- Update to upstream 0.11.2.

* Sat Nov 2 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.11.0-1
- Update to upstream 0.11.0.

* Tue Oct 8 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.10.3-1
- Update to upstream 0.10.3.

* Wed Sep 4 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.10.2-1
- Update to upstream 0.10.2.

* Sun Aug 4 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.10.1-2
- Copy mix binary, too.

* Sat Aug 3 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.10.1-1
- Update to upstream 0.10.1.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.10.0-1
- Update to upstream 0.10.0.

* Wed Jun 12 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.9.3-2
- Fix patch, doctest.exs was renamed to doc_test.exs

* Wed Jun 12 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.9.3-1
- Update to upstream 0.9.3.

* Wed Jun 12 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.9.1-1
- Update to upstream 0.9.1.
- Clean up specfile.

* Sun Feb 17 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.8.1-1
- Update to upstream 0.8.1.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 7 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.7.2-1
- Update to upstream 0.7.2.

* Mon Oct 22 2012 Ricky Elrod <codeblock@fedoraproject.org> - 0.7.0-1.20121022git833e9e9
- Update to upstream 0.7.0.

* Wed Aug 1 2012 Ricky Elrod <codeblock@fedoraproject.org> - 0.6.0-1.20120801git109919c
- Update to upstream 0.6.0.

* Sat May 26 2012 Ricky Elrod <codeblock@fedoraproject.org> - 0.5.0-1.20120526git6052352
- Initial build.
