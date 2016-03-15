#!/usr/bin/env zsh

echo "Removing ~/.zsh link"
if [[ -h ~/.zsh ]]
then
    rm -f ~/.zsh
fi

echo "Looking for original zsh config..."
BACKED_UP_CONFIG=~/.zshrc.ztanesh

if [[ ! -e "$BACKED_UP_CONFIG" ]]
then
    BACKED_UP_CONFIG=~/.zshrc.backup
fi

if [[ -f "$BACKED_UP_CONFIG" || -h "$BACKED_UP_CONFIG" ]]
then
    echo "Restoring $BACKED_UP_CONFIG to ~/.zshrc"

    if [[ -f ~/.zshrc || -h ~/.zshrc ]]
    then
        ZSHRC_SAVE=".zshrc.ztanesh-uninstalled-`date +%Y%m%d%H%M%S`"
        echo "Found ~/.zshrc -- Renaming to ~/${ZSHRC_SAVE}"
        mv ~/.zshrc "~/${ZSHRC_SAVE}"
    fi

    mv "$BACKED_UP_CONFIG" ~/.zshrc

    source ~/.zshrc
else
    echo "Switching back to bash"
    chsh -s /bin/bash
    source /etc/profile
fi

echo "Thanks for trying out ZtaneSH. It's been uninstalled."
