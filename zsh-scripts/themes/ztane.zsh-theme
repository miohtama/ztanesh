#
# Fuuuuck this mess needs clear up and proper annoation.
# Pulling my last hair.
# -Mikko
#
# http://zsh.sourceforge.net/Intro/intro_14.html
#
# http://www.dawoodfall.net/index.php/custom-zsh-prompts
#


# The string here is not actually used.. no idea
PROMPT='%{$fg_bold[green]%}%p %{$fg[cyan]%}%c%{$fg_bold[blue]%}$(git_prompt_info)%{$fg_bold[blue]%} % %{$reset_color%}'

#
# Set Ruby stuff to right side of the prompt
# No idea why this is here... ignored
#
if which rvm-prompt &> /dev/null; then
  RPROMPT='%{$reset_color%} %{$fg[red]%}$(~/.rvm/bin/rvm-prompt i v g) %{$reset_color%}'
else
  if which rbenv &> /dev/null; then
    RPROMPT='%{$reset_color%} %{$fg[red]%}$(rbenv version | sed -e "s/ (set.*$//") %{$reset_color%}'
  fi
fi


#
# Set a special prompt if you are on a server identified by /etc/server-status file
# This is useful e.g. setting a warning message on production servers
#
if [[ -e /etc/server-status ]]
then
    SERVER_STATUS_ENABLED=1
fi

PROMPT_HOSTNAME=`hostname`

#
# Add AWS image name to a prompt
#
IMAGE_NAME=""

if [[ -e /etc/issue ]]
then
    IMAGE_NAME="`grep 'Image:' /etc/issue|sed 's/Image: *\([^ ]\+\).*/\1/'`"
fi

#
# Setup prompt bg color by a server.
#
#
#
function prompt_bg_color_by_server {

}

function setup_prompt {

    # Right side of the prompt
    # Something
    # Bold [
    # Some PROMPT_USER_COLOR
    # %n user
    # PROMPT_HOSTNAME in special PROMPT_HOST_COLOR
    RPROMPT=`echo -ne "%{\033[A%}%{\033[1;37m%}%B[%{\033[${PROMPT_USER_COLOR:-1;33}m%}%n%{\033[0m%}%B@%{\033[${PROMPT_HOST_COLOR:-1;33}m%}$PROMPT_HOSTNAME%b%B][%{\033[1;32m%}%T%b%B]%{\033[B%}"`

    # Left side of the prompt
    # Start bold mode
    # Show git prompt info
    # New line
    # Show the current folder
    PROMPT=`echo -ne '%B$(git_prompt_info)\n%{\033[0m%}%B[%{\033[36m%}%~%b%B]%#'`" "
    # Check that if we are in a Python virtualenv folder
    # but virtualenv is not activatd
    PROPOSED_VIRTUAL_ENV=$(check_unset_venv)
    proposed_envname=`basename "$PROPOSED_VIRTUAL_ENV"`

    if [[ "$SERVER_STATUS_ENABLED" == "1" ]]
    then
        SERVER_STATUS=`xargs echo -ne < /etc/server-status`
        if [[ $SERVER_STATUS == 'LIVE!' ]]
        then
            COLOR="1;5;41;33m"
        else
            COLOR="0;30;46m"
        fi
        if [[ $IMAGE_NAME != '' ]]
        then
            IMAGENAME="%B[%b$IMAGE_NAME%B]%b"
        fi
        PROMPT=`echo -ne "%{\033[1;37m%}[%{\033[$COLOR%}$SERVER_STATUS%{\033[0;37;1m%}]%{\033[0m%}$IMAGENAME"`"$PROMPT"
        unset COLOR
    fi

    if [[ "$VIRTUAL_ENV" != "" ]]
    then
        envname=`basename "$VIRTUAL_ENV"`

        if [[ "$PROPOSED_VIRTUAL_ENV" != "" && "$PROPOSED_VIRTUAL_ENV" != "$VIRTUAL_ENV" ]]
        then
            PROMPT=`echo -ne "%{\033[1;33m%}[%{\033[0;31;43m%}$proposed_envname%{\033[0;33;1m%}]%{\033[0m%}"`"$PROMPT"
        fi

        PROMPT=`echo -ne "%{\033[1;36m%}[%{\033[1;34m%}$envname%{\033[36m%}]%{\033[0m%}"`"$PROMPT"
    else
        if [[ "$proposed_envname" != "" ]]
        then
            PROMPT=`echo -ne "%{\033[1;31m%}[%{\033[0;30;41;5m%}$proposed_envname%{\033[0;31;1m%}]%{\033[0m%}"`"$PROMPT"
        fi
    fi

}

if [[ -x /usr/bin/hostname-filter ]]
then
    PROMPT_HOSTNAME=`/usr/bin/hostname-filter`
fi

setup_prompt


#
# Git repo indicator integration
#
ZSH_THEME_GIT_PROMPT_PREFIX="[%{$fg[red]%}"
ZSH_THEME_GIT_PROMPT_SUFFIX="%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg[yellow]%}✗%{$fg[white]%}]"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg[white]%}]"
