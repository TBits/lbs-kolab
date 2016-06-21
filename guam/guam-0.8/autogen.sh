#!/bin/bash

git reset --hard HEAD
git clean -d -f -x

rm -rf deps/

rebar get-deps
rebar compile
rebar eunit

mkdir deps

pushd rel/
rebar generate
popd

version=$(
        grep '{rel, "kolab_guam", ' rel/reltool.config | sed -r -e 's/^.*([0-9]\.([0-9]+(\.[0-9]+)+)).*$/\1/g'
    )

rm -rf rel/kolab_guam/

tmpdir=${TMPDIR:-/tmp}/guam-${version}

rm -rf ${tmpdir}
mkdir -p ${tmpdir}

cp -a * ./.erlang ${tmpdir}/.

curwd=$(pwd)

pushd $(dirname ${tmpdir})
tar czvf ${curwd}/guam-${version}.tar.gz guam-${version}/
popd

echo "Tarball at guam-${version}.tar.gz"
