#!/bin/bash
#
# Setup nullmailer on Ubuntu using your Gmail account as SMTP
# - you get a working sendmail command without requiring to setup complex SMTP
# stuff. Mostly useful with cron scripts.
#
# Orignal script based on http://www.panticz.de/install-nullmailer
# and https://jon.sprig.gs/blog/post/9
#

#
# Create a gmail SSL wrapper script
#

if [ -n "$GMAIL_USER" || -n "$GMAIL_PASSWORD" || -n "$TEST_ADDRESS" ] ; then
    echo "Usage:"
    echo "GMAIL_USER=foobar@gmail.com GMAIL_PASSWORD=12312312 TEST_ADDRESS=youremail@example.com sh setup-nullmailer.sh"
    exit 1
fi

# install required software
sudo apt-get install -y openssl xinetd nullmailer

sudo tee /usr/bin/gmail-smtp <<EOF >/dev/null
#!/bin/sh
/usr/bin/openssl s_client -connect smtp.gmail.com:465 -quiet 2>/dev/null
EOF
sudo chmod +x /usr/bin/gmail-smtp

#
# Create xinetd.d entry which wraps SMTP traffic to port 10025 go
# go to gmail
#

sudo tee /etc/xinetd.d/gmail-smtp <<EOF >/dev/null
# default: on
# description: Gmail SMTP wrapper for clients without SSL support
# Thanks to http://ubuntuforums.org/showthread.php?t=918335 for this install guide
service gmail-smtp
{
    disable         = no
    bind            = localhost
    port            = 10025
    socket_type     = stream
    protocol        = tcp
    wait            = no
    user            = root
    server          = /usr/bin/gmail-smtp
    type            = unlisted
}
EOF
sudo /etc/init.d/xinetd reload

#
# Set nullmail to use xinetd
#
sudo tee /etc/nullmailer/remotes <<EOF >/dev/null
127.0.0.1 smtp --port=10025 --user=$GMAIL_USER --pass=$GMAIL_PASSWORD
EOF
sudo /etc/init.d/nullmailer reload

# send test email
echo "This is a test message from ${USER}@${HOSTNAME} at $(date)" | sendmail $TEST_ADDRESS
