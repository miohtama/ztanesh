#!/bin/zsh
if [[ `id -u` != "0" ]]
then
    echo "Root required... using sudo"
    exec sudo zsh "$0"
fi

dir=`dirname $0`
(cd /etc/skel && git clone http://haapala.iki.fi/tools/.git)
zsh $dir/setup.zsh /etc/skel
