#!/bin/bash

# parameter: which branch?
if [ -z $1 ]
then
  echo "we need a parameter for the branch"
  echo "sample call: ./$0 Kolab_16"
  exit -1
fi

branch=$1

cd ~
if [ -d rpmbuild ]
then
  mv rpmbuild rpmbuild.bak || exit -1
fi

mkdir -p rpmbuild
mkdir -p rpmbuild/SOURCES
mkdir -p rpmbuild/SPECS
cd rpmbuild
rm -f $branch.tar.gz
wget https://github.com/TBits/lbs-kolab/archive/$branch.tar.gz
tar xzf $branch.tar.gz
cd lbs-kolab-$branch
for d in *
do
  if [ -d $d ]
  then
    for f in $d/*.spec; do
      if [ -f $f ]
      then
        cp $d/*.spec ../SPECS
        rm -Rf $d/debian
        rm -Rf $d/*.spec
        rm -Rf $d/*.dsc
        rm -Rf $d/debian.*
        cp $d/* ../SOURCES
        break
      fi
    done
  fi
done
cd ..
for f in SPECS/*
do
  echo rpmbuild -bs $f
  rpmbuild -bs $f
done

echo "mkdir public_html/kolab/$branch" | sftp tpokorra@fedorapeople.org
for f in SRPMS/*.src.rpm
do
  echo "put $f" | sftp tpokorra@fedorapeople.org:public_html/kolab/$branch
done
