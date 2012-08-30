#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

    Auto-discover log files and generate logrorate config based on it.

    - Find any folders containing log files

    - Add logrotate entry for *.log files in that folder

    - Try to signal Zope application server after log rotation to release the file
      handle and actually release the disk space associated with it

    http://collective-docs.readthedocs.org/en/latest/hosting/zope.html#log-rotate

    http://man.cx/logrotate

    Usage example for Ubuntu / Debian::

        sudo -i -u  # root
        # Generate a log rotate config which is automatically
        # picked up by a log rotate on the next run
        discover-log-rotate /etc/logrotate.d/plone-all /srv/plone

"""

__license__ = "Public domain"
__author__ = "Mikko Ohtamaa <http://opensourcehacker.com>"

import sys

import fnmatch
import os

#: Logroate config template applied for each folder.
#: Modify for your own needs.
TEMPLATE = """
%(folder)s/*.log {
        weekly
        missingok
        # How many days to keep logs
        # In our cases 3 months
        rotate 12
        compress
        delaycompress
        notifempty

        # THE FOLLOWING IS ZOPE SPECIFIC BEHAVIOR

        # This signal will tell Zope to reopen the file-system inode for the log file
        # so it doesn't keep reserving the old log file handle for even if the file is deleted
        # We guess some possible process and PID file names.
        # The process here is little wasfeful, but we don't need to try match a log file to a running process name.
        # TODO: Ideas how to get a process name from the log file name?
        postrotate
            [ ! -f %(installation)s/var/instance.pid ] || kill -USR2 `cat %(installation)s/var/instance.pid`
            [ ! -f %(installation)s/var/client1.pid ] || kill -USR2 `cat %(installation)s/var/client1.pid`
            [ ! -f %(installation)s/var/client2.pid ] || kill -USR2 `cat %(installation)s/var/client2.pid`
            [ ! -f %(installation)s/var/client3.pid ] || kill -USR2 `cat %(installation)s/var/client3.pid`
            [ ! -f %(installation)s/var/client4.pid ] || kill -USR2 `cat %(installation)s/var/client4.pid`
        endscript
}

"""


def run():
    """
    Execute the script.
    """
    if len(sys.argv) < 2:
        sys.exit("Usage: discover-log-rotate [generated config file] [directory]")

    config = sys.argv[1]
    folder = sys.argv[2]

    out = open(config, "wt")

    # Find any folders containing log files
    matches = []
    for root, dirnames, filenames in os.walk(folder):
        for filename in fnmatch.filter(filenames, '*.log'):

            full = os.path.join(root, filename)
            dirpath = os.path.dirname(full)

            if not dirpath in matches:
                matches.append(dirpath)

    for match in matches:

        folder = os.path.abspath(match)

        # Assume the main Zope installation folder is format /srv/plone/xxx
        # and the underlying log folder /srv/plone/xxx/var/log
        installation = os.path.abspath(os.path.join(folder, "../.."))
        cooked = TEMPLATE % dict(folder=match, installation=installation)
        out.write(cooked)

    out.close()

if __name__ == "__main__":
    run()
