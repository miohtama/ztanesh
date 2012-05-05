Ztane supershell powers
--------------------------

Make your ZSH experience feel good.

OSX install commands::

    sudo port install coreutils lesspipe highlight +with_default_names
    git clone git@github.com:miohtama/ztanesh.git ~/tools
    ~/tools/zsh-scripts/setup.zsh

    # Fix missing locale environment variables
    # XXX: Is this problem with every OSX install?
    echo "" > ~/.zsh-local/rc/locales 
    echo "export LC_ALL=en_US.UTF-8" >> ~/.zsh-local/rc/locales
    echo "export LANG=en_US.UTF-8" >> ~/.zsh-local/rc/locales
    comprc

Ubuntu install commands::

    apt-get install git-core highlight zsh
    git clone git@github.com:miohtama/ztanesh.git ~/tools
    ~/tools/zsh-scripts/setup.zsh

Then activat zsh for your user by default::

    usermod -s /bin/zsh root

For root installation you might need to enable SSH agent forwarding for sudo::

    sudo nano /etc/sudoers
    Defaults    env_keep+=SSH_AUTH_SOCK

* http://serverfault.com/questions/107187/sudo-su-username-while-keeping-ssh-key-forwarding