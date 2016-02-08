#!/bin/bash

if [ ! -d "arcanist.git" ]; then
    git clone https://github.com/phacility/arcanist.git arcanist.git
    pushd arcanist.git
else
    pushd arcanist.git
    git remote set-url origin https://github.com/phacility/arcanist.git
    git fetch origin
    git reset --hard origin/master
    git clean -d -f -x
fi

git_short_version_hash=$(git rev-parse --short HEAD)
git_full_version_hash=$(git rev-parse HEAD)

rm -rf ../arcanist-*.tar.gz

git archive --prefix=arcanist-${git_full_version_hash}/ ${git_full_version_hash} | gzip -c > ../arcanist-${git_short_version_hash}.tar.gz

popd

sed -i -r \
    -e "s/git_short_version_hash .*/git_short_version_hash ${git_short_version_hash}/g" \
    -e "s/git_full_version_hash .*/git_full_version_hash ${git_full_version_hash}/g" \
    -e "s/Version: [0-9]+/Version: $(date +'%Y%m%d')/g" \
    arcanist.spec

osc ar
