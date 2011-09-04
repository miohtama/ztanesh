#!/bin/zsh

BASE_DIR="$1"
if [[ "$BASE_DIR" == "" ]]
then
    BASE_DIR=$HOME
fi

if [[ ! -e "$BASE_DIR/.zsh" ]]
then
        if [[ -e $BASE_DIR/tools/zsh-scripts ]]
        then
            ln -s tools/zsh-scripts $BASE_DIR/.zsh
	else
	    echo "$BASE_DIR/.zsh or $BASE_DIR/tools/zsh-scripts - the directory does not exist!"
	    echo "Did you do the git pull properly?"
            exit 1
        fi
fi

ZSHRC="$BASE_DIR/.zshrc"

if [[ -h "$ZSHRC" ]]
then
	rm "$ZSHRC"
elif [[ -e "$ZSHRC" ]]
then
	echo "Backing up old zshrc to zshrc.backup"
	mv "$ZSHRC" "$ZSHRC".backup
fi

echo "Symlinking .zshrc"
ln -s ".zsh/zshrc.template" "$BASE_DIR/.zshrc"

echo "Compiling rc-files"
zsh "$BASE_DIR"/tools/zsh-scripts/scripts/compile.zsh

echo "Checking installed helper programs"
zsh "$BASE_DIR/.zsh/bin/checkinstalledapps" "$BASE_DIR"

echo "All done - enjoy!"
