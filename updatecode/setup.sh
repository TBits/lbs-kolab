#!/bin/bash

if [ -z "$1" ]
then
  echo "please pass parameter for the branch name"
  exit -1
fi

# branch is the name of the project on OBS: eg Kolab:3.4, Kolab:3.4:Updates, Kolab:Development
branch=$1
yum -y install osc git wget || exit -1

cp ~/.ssh/oscrc ~/.oscrc

cd ~
mkdir -p work_$branch
cd work_$branch

eval `ssh-agent`
ssh-add ~/.ssh/gitkey
ssh-keyscan -H github.com >> ~/.ssh/known_hosts
# git does not like colons in branch names...
gitbranch=${branch//:/_}
if [ -d lbs-kolab ]
then
  cd lbs-kolab
  git pull
  cd ..
else
  git clone -b $gitbranch --single-branch --depth 1 git@github.com:TBits/lbs-kolab.git || \
      (git clone -b master --single-branch --depth 1 git@github.com:TBits/lbs-kolab.git && cd lbs-kolab && git checkout -b $gitbranch && git push origin $gitbranch && cd ..) || \
      exit -1
fi

if [ -d osc/$branch ]
then
  cd osc/$branch
  osc update || exit -1
  cd ../..
else
  mkdir -p osc
  cd osc
  osc -A https://obs.kolabsys.com/ checkout --current-dir $branch || exit -1
  cd ..
fi

# do not modify the files in osc directly
rm -Rf osc.work
cp -R osc osc.work
cd osc.work/$branch

for pkgname in *
do
    if [ ! -d $pkgname ]
    then
      continue
    fi

    # do not process all packages, some have huge tar files, too big for Github (eg. erlang-yokozuna/solr-4.10.4.tgz is 143.11 MB, File manticore/manticore-0.1.1.tar.gz is 97.06 MB)
    # check size of files in package
    process=1
    for f in $pkgname/*
    do
      if [ -f $f ]
      then
        size=`stat --printf="%s" $f`
        if [ $size -gt $((50*1024*1024)) ]
        then
          rm -Rf ../../lbs-kolab/$pkgname
          echo "*******************"
          echo "ignoring $pkgname because file $f is too big for Github"
          echo "*******************"
          process=0
        fi
      else
        rm -Rf ../../lbs-kolab/$pkgname
        echo "*******************"
        echo "ignoring $pkgname because it does not contain any files"
        echo "*******************"
        process=0
      fi
    done

    if [ $process -eq 0 ]
    then
      continue;
    fi

    cd $pkgname
    echo "working on $pkgname..."

    debpkgname=$pkgname
    if [[ "$pkgname" == "php-pear-Net-LDAP3" ]]; then
      debpkgname="php-net-ldap3"
    fi

    if [ -f debian.tar.gz ]
    then
      tar xzf debian.tar.gz
      rm -Rf debian.tar.gz
    fi
    if [ -f debian.changelog ]
    then
      mkdir -p debian
      mv debian.changelog debian/changelog
      mv debian.control debian/control
      mv debian.rules debian/rules
    fi
    if [ -f debian.series ]
    then
      mv debian.series debian/series
    fi

    if [ -f $debpkgname.dsc ] 
    then
      if [[ "$debpkgname.dsc" != "${debpkgname,,}"".dsc" ]]
      then
        # make sure that we only have lowercase letters in the dsc filename
        mv $debpkgname.dsc ${debpkgname,,}".dsc"
      fi
    fi

    # check if we need to download the tarball (eg. Kolab 3.4 libkolabxml)
    if [[ "$branch" == "Kolab:3.4" ]]
    then
     if [[ "$pkgname" == "libkolabxml" ]]
     then
      if [ -f ../../../lbs-kolab/libkolabxml/libkolabxml-1.1.tar.gz ]
      then
        cp ../../../lbs-kolab/libkolabxml/libkolabxml-1.1.tar.gz .
      else
        wget https://cgit.kolab.org/libkolabxml/snapshot/libkolabxml-f4a151d78de1a44db6c4b645c753852928664122.tar.gz -O libkolabxml.tar.gz
        tar xzf libkolabxml.tar.gz
        mv libkolabxml-f4a151d78de1a44db6c4b645c753852928664122 libkolabxml-1.1
        tar czf libkolabxml-1.1.tar.gz libkolabxml-1.1
        rm -Rf libkolabxml.tar.gz
        rm -Rf libkolabxml-1.1
      fi
     fi
    fi 

    rm -f _service
    rm -Rf .osc
    cd ..

    rm -Rf ../../lbs-kolab/$pkgname/*
    mkdir -p ../../lbs-kolab/$pkgname
    cp -R $pkgname ../../lbs-kolab/
done

# clean up the temp directory
rm -Rf osc.work

cd ../../lbs-kolab
git add .
git config user.name "LBS BuildBot"
git config user.email tp@tbits.net

TODAY=`date +%Y%m%d`
git commit -a -m "updated $branch to latest version from OBS ($TODAY)"

git push || exit -1
