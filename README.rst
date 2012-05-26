Ztane ZSH
=======================

Take your ZSH experience to the next level.

.. image:: https://github.com/downloads/miohtama/ztanesh/Screen%20shot%202012-05-07%20at%207.52.12%20PM.png

*The screenshot above shows additional ls coloring. Prompt: top left is active virtualenv etc. development environment, top right is server, time, bottom right is path*. 

.. image:: https://github.com/downloads/miohtama/ztanesh/Screen%20Shot%202012-05-22%20at%2011.01.46%20PM.png

*Colorize terminal tabs automatically based on which server you are logged in. No need to preconfigure servers - the color is calculated from the hostname*

Features
------------

* Automatic update mechanism via git to multiple machines

* Colorize terminal tabs based on which server you are connected

* Remote aware autocompletion support for ``scp``, ``svn``

* Readable prompt: bold text by default, timestamps, virtualenv detection, etc.

* Install scripts sets up GNU userland coloring functions, even on OSX

* Special ``ls`` with additional coloring to enhance readabilility

* Global and local .rc settings files. Global settings files shared via Github.

* Settings files are preprocessed by ``comprc`` command for very fast shell start-up

* Dircolors maintained for the latest trends (new source code files, new file formats)

* OSX and Ubuntu/Debian tested 

* Over ten years of running in production experience 

Installation
----------------

For your convenience, fork this repository on Github under your own user account.
The authors are less benevolent dictators of this project and may feel
to change the scripts breaking everything for you any day.

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

    sudo usermod -s /bin/zsh YOURUSENAME

OSX install commands
+++++++++++++++++++++++

Install `GNU userland tools <http://opensourcehacker.com/2012/04/27/python-and-javascript-developer-setup-hints-for-osx-lion/>`_ using 
`Macports <http://macports.org>`_::

    sudo port install perl5 coreutils lesspipe highlight +with_default_names
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


