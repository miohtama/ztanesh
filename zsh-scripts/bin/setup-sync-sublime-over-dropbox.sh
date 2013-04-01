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
        SOURCE="$HOME/.config/sublime-text-2"
else
        echo "Unknown operating system"
        exit 1
fi

# Check that settings really exist on this computer
if [ ! -e "$SOURCE/Packages" ]; then
        echo "Could not find $SOURCE/Packages/"
        exit 1
fi

# Detect that we don't try to install twice and screw up
if [ -L "$SOURCE/Packages" ] ; then
        echo "Dropbox settings already symlinked"
        exit 1
fi

# XXX: Disabled Settings/ folder syncing as looks like
# Sublime keeps only license and .sublime_session files -
# the latter
# which are autosaved and would cause unnecessary conflicts
# and traffic

# Dropbox has not been set-up on any computer before?
if [ ! -e "$SYNC_FOLDER" ] ; then
        echo "Setting up Dropbox sync folder"
        
        # Creating the folders in separated categories
        mkdir -p "$SYNC_FOLDER/Installed Packages"
        mkdir -p "$SYNC_FOLDER/Packages"
#        mkdir -p "$SYNC_FOLDER/Settings"
        
        # Copy the files into their respective folder
        cp -r "$SOURCE/Installed Packages/" "$SYNC_FOLDER/Installed Packages"
        cp -r "$SOURCE/Packages/" "$SYNC_FOLDER/Packages"
#        cp -r "$SOURCE/Settings/" "$SYNC_FOLDER/Settings"
fi

# Now when settings are in Dropbox delete existing files
rm -rf "$SOURCE/Installed Packages"
rm -rf "$SOURCE/Packages"
#rm -rf "$SOURCE/Settings"

# Symlink settings folders from Drobox
# The "Installed Packages" and "Packages" was never
# created inside of Dropbox folder. These lines are not working.
# Fixed to the correct folder.

ln -s "$SYNC_FOLDER/Installed Packages" "$SOURCE/Installed Packages"
ln -s "$SYNC_FOLDER/Packages" "$SOURCE/Packages"
#ln -s "$SYNC_FOLDER/Settings" "$SOURCE/Settings"


