#!/bin/sh

echo "Checking your shell"

(if [[ '1' == '1' ]]
then
    exit 0
fi
exit 1) > /dev/null 2>&1

if test "$?" "!=" "0"
then
    echo "You are using some borken shell, try bash, zsh!"
    exit 1
fi

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

mandatory zsh
mandatory git
optional lesspipe
optional wget
optional highlight

echo "Installation complete."
echo "Checking out new shell files"

mkdir ~/tools
cd ~/tools
git clone https://github.com/miohtama/ztanesh
~/tools/zsh-scripts/setup.zsh
