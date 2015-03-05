#!/bin/bash

tag=v0.2.5

set -e

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$(pwd)

pushd "$tmp"
git clone https://github.com/caolan/async.git
cd async
git archive --prefix="test/" --format=tar tags/${tag}:test/ \
    | bzip2 > "$pwd"/tests-${tag}.tar.bz2
popd
