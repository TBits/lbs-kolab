%if 0%{?opensuse_bs}
#!BuildIgnore:  ghostscript-x11
%endif

%if 0%{?suse_version} < 1 && 0%{?fedora} < 1 && 0%{?rhel} < 7
%global with_systemd 0
%else
%global with_systemd 1
%endif

%{!?_unitdir:   %global _unitdir /usr/lib/systemd/system/}

#
# This package contains only arch-independent data but install it into
# arch-dependent directory thus making this package arch-dependent. In order to
# suppress empty *-debuginfo generation we have to explicitly order
# debuginfo-generator to skip trying to build *-debuiginfo for that package.
#
%global debug_package %{nil}

%define lock_version() %{1}%{?_isa} = %(rpm -q --queryformat "%{VERSION}" %{1})

Name:               riak
Version:            2.1.3
Release:            1%{?dist}
Summary:            Dynamo-inspired key/value store
Group:              Applications/Databases
License:            ASL 2.0
URL:                http://wiki.basho.com/Riak.html
VCS:                https://github.com/basho/riak.git
Source0:            https://github.com/basho/riak/archive/riak-%{version}.tar.gz
Source1:            %{name}.tmpfiles.conf
Source2:            %{name}.init
Source3:            %{name}.service
Source4:            %{name}.conf
Source5:            solr-log4j.properties

Patch1:             riak-2.1.3-no-locking-deps.patch
Patch2:             riak-2.1.3-no-deps-directory.patch
Patch3:             riak-2.1.3-lucene_parser.patch
Patch4:             riak-2.1.1-unvendorize-erl.patch

BuildRequires:      erlang-clique
BuildRequires:	    erlang-cluster_info >= 2.0.2
BuildRequires:	    erlang-ebloom
BuildRequires:	    erlang-eper
BuildRequires:      erlang-ibrowse
BuildRequires:      erlang-lager_syslog >= 2.0.3
BuildRequires:      erlang-meck >= 0.8.2
BuildRequires:      erlang-node_package
BuildRequires:      erlang-pbkdf2
BuildRequires:	    erlang-rebar
BuildRequires:      erlang-riak_auth_mods >= 2.0.1
BuildRequires:	    erlang-riak_control >= 2.1.1
BuildRequires:	    erlang-riak_kv >= 2.1.0
BuildRequires:	    erlang-riak_search >= 2.1.1
BuildRequires:	    erlang-riaknostic >= 2.0.1
BuildRequires:      erlang-syslog
BuildRequires:      erlang-yokozuna >= 2.1.0

#
# Build requirements needed in order to be able to lock versions
#

BuildRequires:      erlang-canola
BuildRequires:      erlang-edown
BuildRequires:      erlang-kvc
BuildRequires:      erlang-parse_trans

#
# Ordinary runtime dependencies
#

Requires:           erlang-bear%{?_isa}
Requires:           erlang-bitcask%{?_isa} >= 1.6.0
Requires:           erlang-ebloom%{?_isa}
Requires:           erlang-eper%{?_isa}
Requires:           erlang-erlydtl%{?_isa}
Requires:           erlang-folsom%{?_isa}
Requires:           erlang-js%{?_isa}
Requires:           erlang-mochiweb%{?_isa}
Requires:           erlang-poolboy%{?_isa}
Requires:           erlang-protobuffs%{?_isa}
Requires:           erlang-sext%{?_isa} >= 1.1

#
# These packages are tightly coupled to the core and
# must be a strict dependencies
#

Requires:           %lock_version erlang-basho_stats
Requires:           %lock_version erlang-bitcask
Requires:           %lock_version erlang-clique
Requires:           %lock_version erlang-cluster_info
Requires:           %lock_version erlang-canola
Requires:           %lock_version erlang-cuttlefish
Requires:           %lock_version erlang-edown
Requires:           %lock_version erlang-eleveldb
Requires:           %lock_version erlang-eper
Requires:           %lock_version erlang-erlydtl
Requires:           %lock_version erlang-exometer_core
Requires:           %lock_version erlang-folsom
Requires:           %lock_version erlang-goldrush
Requires:           %lock_version erlang-ibrowse
Requires:           %lock_version erlang-js
Requires:           %lock_version erlang-kvc
Requires:           %lock_version erlang-lager
Requires:           %lock_version erlang-lager_syslog
# FIXME - I'll add luwak backend later
#Requires:           %lock_version erlang-luwak
Requires:           %lock_version erlang-meck
Requires:           %lock_version erlang-merge_index
Requires:           %lock_version erlang-neotoma
Requires:           %lock_version erlang-parse_trans
Requires:           %lock_version erlang-pbkdf2
Requires:           %lock_version erlang-poolboy
Requires:           %lock_version erlang-protobuffs
Requires:           %lock_version erlang-riak_api
Requires:           %lock_version erlang-riak_auth_mods
Requires:           %lock_version erlang-riak_control
Requires:           %lock_version erlang-riak_core
Requires:           %lock_version erlang-riak_dt
Requires:           %lock_version erlang-riak_ensemble
Requires:           %lock_version erlang-riak_err
Requires:           %lock_version erlang-riak_kv
Requires:           %lock_version erlang-riak_pb
Requires:           %lock_version erlang-riak_pipe
Requires:           %lock_version erlang-riak_search
Requires:           %lock_version erlang-riak_sysmon
Requires:           %lock_version erlang-riaknostic
Requires:           %lock_version erlang-setup
Requires:           %lock_version erlang-sext
Requires:           %lock_version erlang-sidejob
Requires:           %lock_version erlang-syslog
Requires:           %lock_version erlang-yokozuna
Requires:           %lock_version erlang-webmachine

%if 0%{?with_systemd}
%if 0%{?suse_version}
Requires(post):     systemd
Requires(postun):   systemd
Requires(preun):    systemd
%else
Requires(post):     systemd-units
Requires(postun):   systemd-units
Requires(preun):    coreutils
Requires(preun):    systemd-units
%endif
%else
Requires(post):     chkconfig
Requires(post):     initscripts
Requires(postun):   initscripts
Requires(preun):    chkconfig
Requires(preun):    initscripts
%endif
# Users and groups
Requires(pre): shadow-utils


%description
Riak is a Dynamo-inspired key/value store that scales predictably and easily.
Riak also simplifies development by giving developers the ability to quickly
prototype, test, and deploy their applications.

A truly fault-tolerant system, Riak has no single point of failure. No machines
are special or central in Riak, so developers and operations professionals can
decide exactly how fault-tolerant they want and need their applications to be.


%prep
%setup -q -n %{name}-%{name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

sed -i -e 's|cuttlefish/cuttlefish|cuttlefish|g' rel/reltool.config
#sed -i -r -e 's|rel, "riak", "[0-9]+\.[0-9]+\.[0-9]+",|rel, "riak", "%{version}",|g' rel/reltool.config

gzip -d doc/man/man1/*.1.gz
sed -i -e "s,\\\n,,g" doc/man/man1/riak-admin.1

# Override the default vars.config with platform specific settings
cat > rpm.vars.config <<EOF
%% Platform-specific installation paths
{platform_bin_dir,      "%{_bindir}"}.
{platform_data_dir,     "%{_localstatedir}/lib/%{name}"}.
{platform_etc_dir,      "%{_sysconfdir}/%{name}"}.
{platform_base_dir,     "%{_libdir}/%{name}"}.
{platform_lib_dir,      "%{_libdir}/%{name}/lib"}.
{platform_log_dir,      "%{_localstatedir}/log/%{name}"}.

{ring_state_dir,	    "%{_localstatedir}/lib/%{name}/ring"}.
{bitcask_data_root,	    "%{_localstatedir}/lib/%{name}/bitcask"}.
{leveldb_data_root,	    "%{_localstatedir}/lib/%{name}/leveldb"}.

{sasl_error_log,	    "%{_localstatedir}/log/%{name}/sasl-error.log"}.
{sasl_log_dir,		    "%{_localstatedir}/log/%{name}/sasl"}.
{mapred_queue_dir,	    "%{_localstatedir}/lib/%{name}/mr_queue"}.

{web_ip,		        "127.0.0.1"}.
{web_port,		        8098}.
{handoff_port,          8099}.
{pb_ip,			        "127.0.0.1"}.
{pb_port,		        8087}.

{node,                  "riak@127.0.0.1"}.
{crash_dump,            "%{_localstatedir}/log/%{name}/erl_crash.dump"}.

{merge_index_data_root,	"%{_localstatedir}/lib/%{name}/merge_index"}.

{runner_script_dir,     "%{_bindir}"}.
{runner_base_dir,       "%{_libdir}/%{name}"}.
{runner_etc_dir,        "%{_sysconfdir}/%{name}"}.
{runner_log_dir,        "%{_localstatedir}/log/%{name}"}.
{runner_lib_dir,        "%{_libdir}/%{name}"}.
{runner_user,           "riak"}.
{pipe_dir,              "%{_localstatedir}/run/riak/"}.
{app_version,           "%{version}-%{release}"}.
EOF

%build
mkdir -p deps
ln -s %{_libdir}/erlang/lib/bitcask-* deps/bitcask
ln -s %{_libdir}/erlang/lib/cuttlefish-* deps/cuttlefish
ln -s %{_libdir}/erlang/lib/eleveldb-* deps/eleveldb
ln -s %{_libdir}/erlang/lib/lucene_parser-* deps/lucene_parser
ln -s %{_libdir}/erlang/lib/node_package-* deps/node_package
ln -s %{_libdir}/erlang/lib/riak_api-* deps/riak_api
ln -s %{_libdir}/erlang/lib/riak_control-* deps/riak_control
ln -s %{_libdir}/erlang/lib/riak_core-* deps/riak_core
ln -s %{_libdir}/erlang/lib/riak_kv-* deps/riak_kv
ln -s %{_libdir}/erlang/lib/riak_search-* deps/riak_search
ln -s %{_libdir}/erlang/lib/riak_sysmon-* deps/riak_sysmon
ln -s %{_libdir}/erlang/lib/yokozuna-* deps/yokozuna
rebar compile -vv
pushd rel
rebar generate overlay_vars=../rpm.vars.config
popd

%install
# Install Erlang VM config files
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
cp -R rel/%{name}/etc/* %{buildroot}%{_sysconfdir}/%{name}/.

# Install init-script or systemd-service
%if 0%{?with_systemd}
install -D -p -m 0644 %{SOURCE1} %{buildroot}/usr/lib/tmpfiles.d/%{name}.conf
install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
%else
install -D -p -m 0755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
%endif

# Install runtime scripts
install -p -m 0755 -D  rel/%{name}/bin/%{name} %{buildroot}%{_bindir}/%{name}
install -p -m 0755 -D  rel/%{name}/bin/%{name}-admin %{buildroot}%{_bindir}/%{name}-admin
install -p -m 0755 -D  rel/%{name}/bin/search-cmd %{buildroot}%{_bindir}/search-cmd

# Install man-pages
install -d %{buildroot}%{_mandir}/man1/
install -p -m 0644 doc/man/man1/%{name}.1 %{buildroot}%{_mandir}/man1/
install -p -m 0644 doc/man/man1/%{name}-admin.1 %{buildroot}%{_mandir}/man1/
install -p -m 0644 doc/man/man1/search-cmd.1 %{buildroot}%{_mandir}/man1/

# Install remaining Erlang files
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{name}-%{version}/ebin
install -p -m 0644 apps/riak/ebin/%{name}.app %{buildroot}%{_libdir}/erlang/lib/%{name}-%{version}/ebin/
install -p -m 0644 apps/riak/ebin/etop_txt.beam %{buildroot}%{_libdir}/erlang/lib/%{name}-%{version}/ebin/

# Make room for temporary files, logs, and data
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/bitcask/
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/dets/
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/leveldb/
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/merge_index/
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/mr_queue/
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/ring/
mkdir -p %{buildroot}/%{_localstatedir}/log/%{name}/
mkdir -p %{buildroot}/%{_localstatedir}/log/%{name}/sasl/
mkdir -p %{buildroot}/%{_localstatedir}/run/%{name}/

# Install Erlang release binary data
mkdir -p %{buildroot}/%{_libdir}/%{name}/releases/%{version}/
install -m 644 rel/%{name}/releases/RELEASES %{buildroot}/%{_libdir}/%{name}/releases/
install -m 644 rel/%{name}/releases/start_erl.data %{buildroot}/%{_libdir}/%{name}/releases/
install -m 644 rel/%{name}/releases/%{version}/%{name}.boot %{buildroot}/%{_libdir}/%{name}/releases/%{version}/
install -m 644 rel/%{name}/releases/%{version}/%{name}.rel %{buildroot}/%{_libdir}/%{name}/releases/%{version}/
install -m 644 rel/%{name}/releases/%{version}/%{name}.script %{buildroot}/%{_libdir}/%{name}/releases/%{version}/
install -m 644 rel/%{name}/releases/%{version}/start_clean.boot %{buildroot}/%{_libdir}/%{name}/releases/%{version}/
install -m 644 rel/%{name}/releases/%{version}/start_clean.rel %{buildroot}/%{_libdir}/%{name}/releases/%{version}/
install -m 644 rel/%{name}/releases/%{version}/start_clean.script %{buildroot}/%{_libdir}/%{name}/releases/%{version}/

# Install nodetool
install -D -p -m 755 rel/%{name}/erts-*/bin/nodetool %{buildroot}/%{_bindir}/%{name}-nodetool

cp -a rel/%{name}/lib %{buildroot}/%{_libdir}/erlang/lib/%{name}-%{version}/
cd %{buildroot}/%{_libdir}/erlang/lib/%{name}-%{version}/lib/
for mod in $(ls -1d */ | xargs -n 1 basename | grep -v basho-patches); do
    rm -rf $mod
    ln -s %{_libdir}/erlang/lib/$mod $mod
done

# Make compat symlinks
cd %{buildroot}%{_libdir}/%{name}
ln -s %{_libdir}/erlang/lib/riak-%{version}/lib lib

mkdir -p %{buildroot}%{_libdir}/%{name}/erts-6.3/bin
cd %{buildroot}%{_libdir}/%{name}/erts-6.3/bin
ln -s ../../../erlang/erts-6.3/bin/beam beam
ln -s ../../../erlang/erts-6.3/bin/beam.smp beam.smp
ln -s %{_bindir}/cuttlefish cuttlefish
ln -s ../../../erlang/erts-6.3/bin/epmd epmd
ln -s ../../../erlang/erts-6.3/bin/erlexec erlexec
ln -s ../../../erlang/erts-6.3/bin/escript escript
ln -s ../../../../..%{_bindir}/%{name}-nodetool nodetool

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
useradd -r -g %{name} -d %{_localstatedir}/run/%{name} \
-c "Riak - a dynamo-inspired key/value store" %{name} 2>/dev/null || :


%post
%if 0%{?with_systemd}
%systemd_post %{name}.service
%else
/sbin/chkconfig --add %{name}
%endif


%preun
%if 0%{?with_systemd}
%systemd_preun %{name}.service
%else
if [ $1 = 0 ]; then
 /sbin/service %{name} stop > /dev/null 2>&1
 /sbin/chkconfig --del %{name}
fi
%endif


%files
%doc doc/[abdr]* releasenotes/ LICENSE NOTICE README.org RELEASE-NOTES.md THANKS
%if 0%{?with_systemd}
/usr/lib/tmpfiles.d/%{name}.conf
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif
%dir %{_sysconfdir}/%{name}
#%config(noreplace) %{_sysconfdir}/%{name}/app.config
#%config(noreplace) %{_sysconfdir}/%{name}/vm.args
%config(noreplace) %{_sysconfdir}/%{name}/riak.conf
%config(noreplace) %{_sysconfdir}/%{name}/solr-log4j.properties
%{_bindir}/%{name}
%{_bindir}/%{name}-admin
%{_bindir}/%{name}-nodetool
%{_bindir}/search-cmd
%dir %{_libdir}/erlang/lib/%{name}-%{version}
%dir %{_libdir}/erlang/lib/%{name}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{name}-%{version}/lib
%{_libdir}/erlang/lib/%{name}-%{version}/ebin/%{name}.app
%{_libdir}/erlang/lib/%{name}-%{version}/ebin/etop_txt.beam
%{_libdir}/erlang/lib/%{name}-%{version}/lib/*
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man1/%{name}-admin.1.gz
%{_mandir}/man1/search-cmd.1.gz
%{_libdir}/%{name}/
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/lib/%{name}/
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/lib/%{name}/bitcask/
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/lib/%{name}/dets/
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/lib/%{name}/leveldb/
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/lib/%{name}/merge_index/
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/lib/%{name}/mr_queue/
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/lib/%{name}/ring/
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/log/%{name}/
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/log/%{name}/sasl/
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/run/%{name}/


%changelog
* Fri Jan  1 2016 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.1.3-1
- Check in 2.1.3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Oct 28 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.2-2
- Rebuild with new Erlang
- Hopefully fix #986623

* Tue Aug 06 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.2-1
- Ver. 1.3.2
- Raised a number of opened files/sockets to 16384
- Install nodetool into _bindir/
- Don't use versioned path to escript to simplify updates in the future
- Use systemd macros

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 08 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.1-2
- Fix broken lager config

* Sat Apr 06 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.1-1
- Ver. 1.3.1

* Sun Mar 24 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.3.1-0.1.rc1
- Ver. 1.3.1rc1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Nov 18 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.2.1-1
- Ver. 1.2.1

* Tue Aug 14 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.4-2
- Fixed lots of packaging issues (thanks to Ankur Sinha for noticing them)

* Fri Jul 20 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.4-1
- Ver. 1.1.4

* Wed Oct 13 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.13.0-1
- Initial build

