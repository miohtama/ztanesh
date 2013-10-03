#!/bin/sh
#
# Set-up Sublime settings + packages sync over Dropbox
#
# Will sync settings + Installed plug-ins
#
# Tested on OSX - should support Linux too as long as
# you set-up correct SOURCE folder
#
# Copyright 2012 Mikko Ohtamaa http://opensourcehacker.com
# Licensed under WTFPL
#

# Note: If there is an existing installation in Dropbox,
# it will replace settings on a local computer

# No Warranty! Use on your own risk. Take backup of Library/Application Support/Sublime Text 2 folder first.

DROPBOX="$HOME/Dropbox"

# Where do we put Sublime settings in our Dropbox
SYNC_FOLDER="$DROPBOX/Sublime"

# Where Sublime settings have been installed
if [ `uname` = "Darwin" ];then
        SOURCE="$HOME/Library/Application Support/Sublime Text 2"
elif [ `uname` = "Linux" ];then
		if [ -e $HOME/.config/sublime-text-3 ]; then
				SOURCE="$HOME/.config/sublime-text-3"
		elif [ -e $HOME/.config/sublime-text-2 ]; then
				SOURCE="$HOME/.config/sublime-text-2"
		else
				echo "Unknown SublimeText version"
				exit 1
		fi
else
        echo "Unknown operating system"
        exit 1
fi

# Check that settings really exist on this computer
if [ ! -e "$SOURCE/Packages" -o ! -e "$SOURCE/Installed Packages" ]; then
        echo "Could not find SublimeText setup files!"
        exit 1
fi

# SublimeText has not been set up on Dropbox?
if [ ! -e "$SYNC_FOLDER" ]; then
        echo "Setting up Dropbox sync folder"
        mkdir -p "$SYNC_FOLDER/"
fi

# Dropbox not populated, copy from this computer.
if [ ! -e "$SYNC_FOLDER/Installed Packages" ]; then
		cp -r "$SOURCE/Installed Packages" "$SYNC_FOLDER/"
fi
if [ ! -e "$SYNC_FOLDER/Packages" ]; then
		cp -r "$SOURCE/Packages" "$SYNC_FOLDER/"
fi

# Detect that we don't try to install twice and screw up
if [ -L "$SOURCE/Packages" -o -L "$SOURCE/Installed Packages" ] ; then
        echo "Dropbox folders already symlinked"
        exit 1
fi

# Rename the local copies.
mv "$SOURCE/Installed Packages" "$SOURCE/Installed Packages.old"
mv "$SOURCE/Packages" "$SOURCE/Packages.old"

# Symlink folders from Drobox.
ln -s "$SYNC_FOLDER/Installed Packages" "$SOURCE/Installed Packages"
ln -s "$SYNC_FOLDER/Packages" "$SOURCE/Packages"

