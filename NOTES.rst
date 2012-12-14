Misc notes
============

Other best practices
----------------------

`Python and Javascript developer setup hints for OSX Lion <http://opensourcehacker.com/2012/04/27/python-and-javascript-developer-setup-hints-for-osx-lion/>`_  


Sudo + SSH forwards
----------------------

For root installation you might need to enable SSH agent forwarding for sudo::

    sudo nano /etc/sudoers
    Defaults    env_keep+=SSH_AUTH_SOCK

* http://serverfault.com/questions/107187/sudo-su-username-while-keeping-ssh-key-forwarding
