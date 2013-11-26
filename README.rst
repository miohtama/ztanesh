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


Oh my ZSH
----------------------

As of December 14, 2012, an attempt to merge the code with the `Oh my zsh <https://github.com/robbyrussell/oh-my-zsh>`_ code started, due to the
enormous amount of plugins readily available for the latter project. The goal is to merge the both projects into something where the startup
files could be automatically compiled and catenated for superfast startup as is done for the ztanesh currently, while enabling the drop-in
use of Oh my zsh plugins and themes.

Features
------------

Out of the box you will be able to

* **Colorize** command line while you are typing it (based on `zsh-syntax-highlighting <https://github.com/zsh-users/zsh-syntax-highlighting/>`_)

* **Colorize** terminal tabs based on SSH connection. Each server automatically gets its own color. (iTerm2)

* Automatically update the window title on your terminal based on the currently running command etc.

* Just type in the directory name on the command prompt to enter into it. Cdable environment variables for fast navigation -
  instead of ``cd $MYDIR/project`` you can now hit in shell prompt ``MY<TAB>p<TAB>``.

* In-word completions - to cd into that ``linux-2.6.28 folder``, just type ``28<TAB>`` - the only matching word is automatically completed.
  To go to ``/usr/bin`` type in shell prompt ``/u/b<TAB>`` (no **cd** needed).

* Double-tap TAB for **autocompletion menu with arrow navigation**. Type ``./<TAB>`` to
  start file explorer in the current folder. Press space to advance the next folder.
  Press backspace to undo the selection.

* **Autocompletion for remote server commands** like *svn*, *scp*

* **Typo correction** when autocompleting: wrong case, mispelt character, etc.

* **Improved prompt readability**: bold text by default, timestamps, user, server name and smart current working directory indicator

* Turn on colored output for tools like *less* and *grep* automatically

* **Improved ls output colors** - including grouping filesizes in groups of 3.

* Settings files are preprocessed for **fast shell start-up**

* **Mouse support on command line**; press alt-m (meta-m) to toggle mouse mode and
  enable position text edit cursor with the mouse

* **Forward- and backward moving in directories stack** using alt+left/right arrows (Linux only)

* **Support for Mac standard edit keys**: *alt+arrow* to move between words. *fn+arrow* (home, end)
  to go to the beginning and end of the line

* **Automatic update** via Github. Global (across machines, autoupdated) and local (macine specific) .rc settings files

* **Over ten years** of running in production experience

* **Upcoming:** intershell clipboard using a pure python X client (you need X forwarding and X11 daemon
  on an originating computer. Launching local commands from remote commandline over ssh X11 forwarding.

Installation
----------------

The installation instructions are based on the assumption you checkout Git repository under `~/tools` folder
in your home directory.


OSX
+++++++++++++++++++++++

Install `GNU userland tools <http://opensourcehacker.com/2012/04/27/python-and-javascript-developer-setup-hints-for-osx-lion/>`_ using
`Macports <http://macports.org>`_::

    brew install zsh coreutils lesspipe findutils highlight

Clone ztanesh::

    git clone git://github.com/h25/ztanesh.git ~/tools
    ~/tools/zsh-scripts/setup.zsh

Test that ZSH starts properly::

    zsh

Activate zsh for your user account as the default shell::

    sudo dscl . -create /Users/YOURUSERNAME UserShell /usr/local/bin/zsh


Usage
-------------

Misc tips
+++++++++++++++++++++++

* See various aliases

* Use CTRL+R to search shared ZSH history

Editing global settings
+++++++++++++++++++++++

ZtaneSH scripts are located in ``~/tools/zsh-scripts/rc`` folder. They are
processed pretty much like ``init.d`` scripts (loaded in number prefix order).

Edit these source scripts.
Then run ``comprc``. This will update ``~/tools/zsh-scripts/var/compiled/allrcs`` file.
This file is optimized ZSH script output and loaded on every start up.

Push your changes to Github.

Editing local settings
+++++++++++++++++++++++++

Put your local settings to ``~/.zsh-local/rc``
and run ``comprc`` alias to make them effective for the next zsh startup.

Community
-----------

IRC
++++

Join us at *#ztanesh* on irc.freenode.org.

Submitting patches
++++++++++++++++++++

1) Press *Fork* button on Github -> creates your personal ZtaneSH repo on github.com

2) Checkout your personal repo as ~/tools

       git clone git@github.com:xxx/ztanesh.git # Your personal repo address

3) Edit files

4) Commit changes, push back to your personal repo

       git add -A
       git commit -m "Why I did this"
       git push

5) On your personal Github repo page, press Make pull request button

Related projects
---------------------

* `Presto <https://github.com/sorin-ionescu/prezto>`_

* `Oh my ZSH <https://github.com/robbyrussell/oh-my-zsh/>`_ - integrated with ZtaneSH

Troubleshooting
------------------

If ZSH does not start up properly (CTRL+C interruption, Git update failure, etc.) you may see the error::

    /Users/mikko/.zsh//lib/ztanesh-rcs.zsh:103: command not found: rainbow-parade.py

You can fix this issue by enabling ``comprc`` function by hand and run it to rebuild startup files::

    source ~/tools/zsh-scripts/rc/03-functions
    comprc

License
----------

`GPL3+ <http://www.gnu.org/licenses/gpl-3.0.html>`_.

Authors
---------

* Antti "ztane" Haapala

* Cleaned up for public release by `Mikko Ohtamaa <http://opensourcehacker.com>`_

* mouse.zsh: Stephane Chazelas

* Gentoo: Alberto Zuin

