"""

    Firebug - Sublime Text 2 connector.

    Allows you to open any Firebug files in Sublime Text 2 text editor.
    Maps URLs to files.

    Usage::

        firebug-subl [url] [line-no] [base-url] [base-directory]

    Example configuration line in Firebug editor settings::

        firebug-subl %url %line http://localhost:8000 ~/code/mixnap-base/krusovice-src

    Shell expansion supported.

    Starting Firefox from command-line for debugging::

        /Applications/Firefox.app/Contents/MacOS/firefox

    Because of Firebug's retardness this script must be wrapped with py2app on OSX.
    In clean virtualenv::

        # We need py2app trunk version for OSX Mountain Lion as the writing of this (altgraph > 0.10)
        # First install hg command (mercurial)
        pip install setuptools-hg
        pip install -e hg+https://bitbucket.org/ronaldoussoren/altgraph#egg=altgraph
        pip install -e hg+https://bitbucket.org/ronaldoussoren/macholib#egg=macholib
        pip install -e hg+https://bitbucket.org/ronaldoussoren/modulegraph#egg=modulegraph
        pip install -e hg+https://bitbucket.org/ronaldoussoren/py2app#egg=py2app
        py2applet firebug-subl.py

    Install on OSX::

        cd /Applications
        sudo ln -s ~/tools/zsh-scripts/bin/firebug-subl.app .

"""

__author__ = "Mikko Ohtamaa <http://opensourchacker.com>"
__license__ = "MIT"

import os
import sys
import subprocess
import logging

# Write debug output to a file as we don't otherwise get any feedback
# if this script fails
logger = logging.getLogger("firebug-subl")
hdlr = logging.FileHandler('/tmp/firebug-subl.log')
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# Add your installation here if missing
LOCATIONS = [
    "C:\\Program Files\\Sublime Text 2\\sublime_text.exe",
    "/home/ed/apps/sublime_text_2/sublime_tex",
    "/Applications/Sublime Text 2.app/Contents/SharedSupport/bin/subl"
    "/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl"
]


def guess_subl():
    """
    Guess the editor location.
    """
    for loc in LOCATIONS:
        if os.path.exists(loc):
            return loc

    return None


def main():
    """
    Main magic.
    """
    # Where subl lives?
    editor = guess_subl()

    # Read command-line
    url, line, base_url, base_dir = sys.argv

    # Map Javascript file location from URL to a file on a disk
    path = url.replace(base_url, base_dir)

    # Create a Sublime Text 2 style direct line in a file pointer
    hint = path + ":" + line

    # Call Sublime Text to open the file in the current project.
    # Create process with shell variable expansion
    subprocess.call([editor, hint], shell=True)

try:
    main()
except Exception as e:
    logger.exception(e)


