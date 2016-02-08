#!/bin/bash

if [ ! -d "libphutil.git" ]; then
    git clone https://github.com/phacility/libphutil.git libphutil.git
    pushd libphutil.git
else
    pushd libphutil.git
    git remote set-url origin https://github.com/phacility/libphutil.git
    git fetch origin
    git reset --hard origin/master
    git clean -d -f -x
fi

git_short_version_hash=$(git rev-parse --short HEAD)
git_full_version_hash=$(git rev-parse HEAD)

rm -rf ../libphutil-*.tar.gz

git archive --prefix=libphutil-${git_full_version_hash}/ ${git_full_version_hash} | gzip -c > ../libphutil-${git_short_version_hash}.tar.gz

popd

sed -i -r \
    -e "s/git_short_version_hash .*/git_short_version_hash ${git_short_version_hash}/g" \
    -e "s/git_full_version_hash .*/git_full_version_hash ${git_full_version_hash}/g" \
    -e "s/Version: [0-9]+/Version: $(date +'%Y%m%d')/g" \
    libphutil.spec

osc ar
