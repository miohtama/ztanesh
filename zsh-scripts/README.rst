Ztane supershell powers
--------------------------

OSX install commands::

    sudo port install coreutils lesspipe highlight +with_default_names
	git clone git@github.com:miohtama/ztanesh.git ~/tools
	~/tools/zsh-scripts/setup.zsh

Add to .zshrc::

    export PATH=/opt/local/libexec/gnubin:/opt/local/bin:/opt/local/sbin:$PATH
    export CLICOLOR=1
    export LESSOPEN='| /opt/local/bin/lesspipe.sh %s'
