Ztane supershell powers
--------------------------

Take your ZSH experience to the next level.
=======


.. image:: https://github.com/downloads/miohtama/ztanesh/Screen%20shot%202012-05-07%20at%207.52.12%20PM.png

*The screenshot above shows additional ls coloring. Prompt: top left is active virtualenv etc. development environment, top right is server, time, bottom right is path*. 

Features
------------

* Very good prompt

* Set-up GNU userland coloring functions

* Special ``ls`` with additional coloring

* Automatic updates

* Global and local RC files 

* OSX and Ubuntu/Debian tested 

* Automatic update mechanism via git to multiple machines

* Remote autocompletion support for ``scp``, ``svn``

* Readable prompt: bold text by default, timestamps, virtualenv detection, etc.

* Install scripts sets up GNU userland coloring functions

* Special ``ls`` with additional coloring to enhance readabilility

* Global (shared between machines) and local .rc settings files 

* Settings files are preprocessed by ``comprc`` command for very fast start-up

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

Ubuntu install commands::

    apt-get install git-core highlight zsh perl
    git clone git@github.com:miohtama/ztanesh.git ~/tools
    ~/tools/zsh-scripts/setup.zsh

Then activate zsh for your user by default::

    usermod -s /bin/zsh root

Put other local settings to ``~/.zsh-local/rc`` 
and run ``comprc`` alias.

Misc
------

For root installation you might need to enable SSH agent forwarding for sudo::

    sudo nano /etc/sudoers
    Defaults    env_keep+=SSH_AUTH_SOCK

* http://serverfault.com/questions/107187/sudo-su-username-while-keeping-ssh-key-forwarding

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
