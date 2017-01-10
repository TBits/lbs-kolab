#!/bin/bash

dnf install -y python-setuptools make graphviz-python graphviz-gd python-pillow python-sphinx python-sphinx-latex git which
git clone --depth 1 http://git.kolab.org/diffusion/D/docs.git
cd docs

make html

#upload to Hostsharing
if [ -f ~/.ssh/id_rsa_cronjob ]
then
  rsync -avz --delete -e "ssh -o 'StrictHostKeyChecking no' -i ~/.ssh/id_rsa_cronjob" build/html tim00-timotheus@tim00.hostsharing.net:kolabdocs
fi

make latexpdf

#upload to Hostsharing
if [ -f ~/.ssh/id_rsa_cronjob ]
then
  rsync -avz --delete -e "ssh -o 'StrictHostKeyChecking no' -i ~/.ssh/id_rsa_cronjob" build/latex/KolabGroupware.pdf tim00-timotheus@tim00.hostsharing.net:kolabdocs
fi
