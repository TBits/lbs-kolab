#!/bin/bash

tar zxvf eimap-*.*.*.tar.gz
target=$(ls -1d eimap-*.*.*/ | xargs -n 1 basename | sed -e 's/eimap/erlang-eimap/g')
rm -rf eimap-*.*.*.tar.gz
rm -rf ${target}
mv eimap-*.*.* ${target}
tar czvf ${target}.tar.gz ${target}
