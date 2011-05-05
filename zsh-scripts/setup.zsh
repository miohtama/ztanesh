#!/bin/zsh

if [[ ! -e ~/.zsh ]]
then
        if [[ -e ~/tools/zsh-scripts ]]
        then
            ln -s ~/tools/zsh-scripts ~/.zsh
	else
	    echo ~/.zsh tai ~/tools/zsh-scripts "- the directory does not exist!"
	    echo "Did you do the git pull properly?"
            exit 1
        fi
fi

if [[ -h ~/.zshrc ]]
then
	rm ~/.zshrc
elif [[ -e ~/.zshrc ]]
then
	echo "Backing up old zshrc to zshrc.backup"
	mv ~/.zshrc ~/zshrc.backup
fi

echo "Symlinking .zshrc"
ln -s ~/.zsh/zshrc.template ~/.zshrc

echo "Compiling rc-files"
zsh ~/.zsh/scripts/compile.zsh

echo "Checking installed helper programs"
zsh ~/.zsh/bin/checkinstalledapps

echo "All done - enjoy!"
