Introduction
----------------------

Improve your UNIX command line experience and productivity with the  
the configuration provided by **ztanesh** project: the tools
will make your shell more powerful and easier to use.

.. contents :: 

.. image:: https://github.com/downloads/miohtama/ztanesh/Screen%20shot%202012-05-07%20at%207.52.12%20PM.png

*The screenshot above shows additional ls coloring. Prompt: top left is active virtualenv etc. development environment, top right is server, time, bottom right is path*.

.. image:: https://github.com/downloads/miohtama/ztanesh/Screen%20Shot%202012-05-22%20at%2011.01.46%20PM.png

*Colorize terminal tabs automatically based on which server you are logged in. No need to preconfigure servers - the color is calculated from the hostname*


Features
------------

* **Colorize** terminal tabs based on SSH connection. Each server automatically gets its own color. (iTerm2, KDE)

* **No need for cd**: just type in the directory name on the command prompt to enter into it. Cdable environment variables for fast navigation.

* Double-tap TAB for **autocompletion menu with arrow navigation**. Type ./ [TAB] to
  start file explorer in the current folder. Press space to advance the next folder.
  Press backspace to undo the selection.

* **Autocompletion for remote server commands** like *svn*, *scp*

* **Improved prompt readability**: bold text by default, timestamps, user, server name and smart current working directory indicator

* Turn on colored output for tools like *less* and *grep* 

* **Improved *ls* output colors**

* Settings files are preprocessed for **fast shell start-up**

* **Mouse support on command line**; press alt-m (meta-m) to toggle mouse mode and 
  enable position text edit cursor with the mouse 

* **Forward- and backward moving in directories stack** using alt+left/right arrows (Linux only)

* **Support for Mac standard edit keys**: *alt+arrow* to move between words. *fn+arrow*
  to go to the beginning and end of the line
  
* **Automatic update** via Github. Global (across machines, autoupdated) and local (macine specific) .rc settings files

* **Over ten years** of running in production experience

Installation
----------------

For your convenience, fork this repository on Github under your own user account, or 
set up your own private fork on anywhere you want. The authors are less benevolent dictators 
(read: BOFHs) of this project and may feel to change the scripts breaking everything for you any day.

But you can also feel free to hack this project into pieces. If you find good patches
just make Pull request on Github.

**The installation instructions are based on the assumption you checkout Git repository under ~/tools folder**.

Ubuntu
++++++

Ubuntu install commands::

    sudo apt-get install git-core highlight zsh perl
    git clone git://github.com/miohtama/ztanesh.git ~/tools
    ~/tools/zsh-scripts/setup.zsh

Test that ZSH starts properly::

    zsh

Then activat zsh for your user by default::

  chsh -s /bin/zsh $USER

... or for the other users::

    sudo usermod -s /bin/zsh TARGETUSERNAME

Gentoo
+++++++

Gentoo Linux install commands::

    sudo emerge -av git highlight zsh
    git clone git://github.com/miohtama/ztanesh.git ~/tools
    ~/tools/zsh-scripts/setup.zsh

Test that ZSH starts properly::

    zsh

Then activat zsh for your user by default::

  chsh -s /bin/zsh $USER

... or for the other users::

    sudo usermod -s /bin/zsh TARGETUSERNAME


OSX (Macports)
+++++++++++++++++++++++

Install `GNU userland tools <http://opensourcehacker.com/2012/04/27/python-and-javascript-developer-setup-hints-for-osx-lion/>`_ using
`Macports <http://macports.org>`_::

    sudo port install perl5 coreutils lesspipe findutils highlight grep +with_default_names
    git clone git://github.com/miohtama/ztanesh.git ~/tools
    ~/tools/zsh-scripts/setup.zsh

Test that ZSH starts properly::

    zsh

Then you MIGHT want to `fix locales for OSX <http://const-cast.blogspot.com/2009/04/mercurial-on-mac-os-x-valueerror.html>`_::

    # Fix missing locale environment variables on OSX
    # XXX: Is this problem with every OSX install or just me?
    echo "" > ~/.zsh-local/rc/locales
    echo "export LC_ALL=en_US.UTF-8" >> ~/.zsh-local/rc/locales
    echo "export LANG=en_US.UTF-8" >> ~/.zsh-local/rc/locales
    comprc

Activate zsh for your user account as the default shell::

    sudo dscl . -create /Users/YOURUSERNAME UserShell /opt/local/bin/zsh

Other 'NIX operating systems
++++++++++++++++++++++++++++++

Other UNIX flavour operating systems should work just fine. Please adjust the installation
commands according to your distribution and `report back to us how you did it <https://github.com/miohtama/ztanesh/issues>`_.

Usage
-------------

Misc tips
+++++++++++++++++++++++

* See various aliases

* Use CTRL+R to search shared ZSH history

Editing global settings
+++++++++++++++++++++++

Edit ``~/tools/zsh-scripts/rc`` files.

Run ``comprc``.

Push your changes to Github.

Editing local settings
+++++++++++++++++++++++++

Put your local settings to ``~/.zsh-local/rc``
and run ``comprc`` alias to make them effective for the next zsh startup.

License
----------

`GPL3+ <http://www.gnu.org/licenses/gpl-3.0.html>`_.

Authors
---------

* Antti "ztane" Haapala

* Cleaned up for public release by `Mikko Ohtamaa <http://opensourcehacker.com>`_

* mouse.zsh: Stephane Chazelas

* Gentoo: Alberto Zuin

