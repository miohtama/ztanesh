#!/usr/bin/env python
"""

       Set terminal tab / decoration color by server name

"""

import socket
import binascii
import random
import colorsys
import sys

# http://stackoverflow.com/questions/1523427/python-what-is-the-common-header-format
__copyright__ = "Copyright 2012 Mikko Ohtamaa - http://opensourcehacker.com"
__author__ = "Mikko Ohtamaa <mikko@opensourcehacker.com>"
__licence__ = "WTFPL"
__credits__ = ["Antti Haapala"]

USAGE = """
Colorize terminal tab based on the current host name.

Usage: rainbow-parade.py [0-1.0] [0-1.0] # Lightness and saturation values

An iTerm 2 example (recolorize dark grey background and black text):

    rainbow-parade.py 0.7 0.4
"""


def get_random_by_string(s, min, max):
    """
    Get always the same random number based on an arbitrary string
    """

    # Calculate CRC32 for the string
    seed = binascii.crc32(s)
    random.seed(seed)
    return random.randrange(min, max)


def decorate_terminal(color):
    """
    Set terminal tab / decoration color.

    Please note that iTerm 2 / Konsole have different control codes over this.
    Note sure what other terminals support this behavior.

    :param color: tuple of (r, g, b)
    """

    r, g, b = color

    # iTerm 2
    # http://www.iterm2.com/#/section/documentation/escape_codes"
    sys.stderr.write("\033]6;1;bg;red;brightness;%d\a" % int(r * 255))
    sys.stderr.write("\033]6;1;bg;green;brightness;%d\a" % int(g * 255))
    sys.stderr.write("\033]6;1;bg;blue;brightness;%d\a" % int(b * 255))

    # Konsole
    # TODO
    # http://meta.ath0.com/2006/05/24/unix-shell-games-with-kde/


def rainbow_unicorn(lightness, saturation):
    """
    Colorize terminal tab by your server name.

    Create a color in HSL space where lightness and saturation is locked, tune only hue by the server.

    http://games.adultswim.com/robot-unicorn-attack-twitchy-online-game.html
    """

    name = socket.gethostname()

    hue = get_random_by_string(name, 0, 1)

    color = colorsys.hls_to_rgb(hue, lightness, saturation)

    decorate_terminal(color)


def main():
    """
    From Toholampi with love http://www.toholampi.fi/tiedostot/119_yleisesite_englanti_naytto.pdf
    """
    if(len(sys.argv) < 3):
        sys.exit(USAGE)

    lightness = float(sys.argv[1])
    saturation = float(sys.argv[2])

    rainbow_unicorn(lightness, saturation)

if __name__ == "__main__":
    main()
