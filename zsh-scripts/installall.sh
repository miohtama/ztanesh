#!/bin/sh

echo -n "Checking which installation program to use: "

if which apt-get
then
	INSTCMD="apt-get install"
elif which yast
then
	INSTCMD="yast -i"
fi

echo "Installing necessary commands... "

function doinstall {
    echo -ne "  * $1... "
    which "$1" > /dev/null 2>&1
    if [[ "$?" == "0" ]]
    then
        echo "installed."
        return
    fi
    echo "not installed."
    sudo $INSTCMD $1
}

function mandatory {
    doinstall $1
    if [[ "$?" != "0" ]]
    then
        echo "Error 1: Installation of $1 failed" >&2
        exit 1
    fi
}

function optional {
    doinstall $1
}

mandatory zsha
mandatory git
optional lesspipe
optional wget
optional highlight

echo "Installation complete."
echo "Checking out new shell files"

git pull http://haapala.iki.fi/tools ~/tools
~/tools/setup.zsh
