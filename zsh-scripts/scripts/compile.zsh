#!/usr/bin/env zsh

export LOCALRC=~/.zsh-local/rc
export GLOBALRC=~/.zsh/rc
export ALLRCS=$GLOBALRC/../compiled/allrcs

if mkdir -p ~/.zsh-local/rc 2>&1 > /dev/null 
then
    touch ~/.zsh-local/rc/placeholder
fi

zsh -c '
	echo "" > $ALLRCS

	startfiles=`\ls -1 $LOCALRC/* $GLOBALRC/* | xargs -n 1 basename | sort | uniq`

	for i in `echo $startfiles`
	do
	        if [[ -e $LOCALRC/$i ]]
	        then
			cat $LOCALRC/$i >> $ALLRCS
	        else
			cat $GLOBALRC/$i >> $ALLRCS
        	fi
	done
'

sleep 2
zcompile $ALLRCS
