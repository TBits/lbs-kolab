#!/bin/bash

# parameter: which branch?
if [ -z $1 ]
then
  echo "we need a parameter for the branch"
  echo "sample call: ./$0 Kolab_3.4"
  echo "sample call: ./$0 Kolab_16"
  exit -1
fi

branch=$1

packages="libcalendaring libkolabxml libkolab kolab-utils php-Net-LDAP3 roundcubemail roundcubemail-skin-chameleon roundcubemail-plugins-kolab roundcubemail-plugin-contextmenu kolab-webadmin kolab pykolab chwala iRony kolab-freebusy kolab-syncroton kolab-schema kolab-autoconf cyrus-imapd"

function want_this_package {
  result=false
  for p in $packages
  do
    if [ "$1" == "$p.spec" ]
    then
      result=true
      break
    fi
  done
}

function prepare_srpm {
  branch=$1
  cd ~/rpmbuild
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
          if [ ! -f ~/rpmbuild/SPECS/`basename $f` ]
          then
            want_this_package `basename $f`
            if [ "$result" == "true" ]
            then
              echo "prepare package " `basename $f`
              cp $d/*.spec ../SPECS
              rm -Rf $d/debian
              rm -Rf $d/*.spec
              rm -Rf $d/*.dsc
              rm -Rf $d/debian.*
              cp $d/* ../SOURCES
              break
            fi
          fi
        fi
      done
    fi
  done
  cd ..
}

# run this now. so that we get reminded to load the ssh key
error=0
echo "mkdir public_html/kolab/$branch" | sftp tpokorra@fedorapeople.org || error=1
if [ $error -eq 1 ]
then
  echo "please load the ssh key"
  exit -1
fi

cd ~
if [ -d rpmbuild ]
then
  mv rpmbuild rpmbuild.bak || exit -1
fi

mkdir -p rpmbuild
mkdir -p rpmbuild/SOURCES
mkdir -p rpmbuild/SPECS

if [ "$branch" == "Kolab_3.4" ]
then
  prepare_srpm Kolab_3.4_Updates
  prepare_srpm Kolab_3.4
else
  prepare_srpm $branch
fi

for f in SPECS/*
do
  echo rpmbuild -bs $f
  rpmbuild -bs $f || exit -1
done

for f in SRPMS/*.src.rpm
do
  echo "uploading $f..."
  echo "put $f" | sftp tpokorra@fedorapeople.org:public_html/kolab/$branch
done
