#!/usr/bin/env python2

# peacock - Pretty Enhanced Arbitrary Command Output Coloring Kit
#
# Python port of acoc
#
# Version : 0.1
# Author : Antti Haapala <antti@haapala.name>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation under version 3, or (at your option)
#   any later version.
# 
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
# 
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#    
#
# Originally based on the Ruby language version by Ian McDonald,
#
# $Id: acoc,v 1.67 2005/02/27 01:02:24 ianmacd Exp $
#
# Version : 0.7.1
# Author  : Ian Macdonald <ian@caliban.org>
# 
# Copyright (C) 2003-2005 Ian Macdonald
# 
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2, or (at your option)
#   any later version.
# 
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
# 
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from __future__ import with_statement

"""
peacock
====

peacock is a regular expression based color formatter for programs that
display output on the command-line. It works as a wrapper around the target
program, executing it and capturing the stdout stream. Optionally, stderr can
be redirected to stdout, so that it, too, can be manipulated.

peacock then applies matching rules to patterns in the output and applies
color sets to those matches. If the ACOC environment variable is set
to 'none', peacock will not perform any coloring.

OPTIONS
--------

These will be enabled in the future:

-h or --help
  Display usage information.
-v or --version
  Display version information.

AUTHORS
-------

Python port written by Antti Haapala <antti@haapala.name>

Pseudo-terminal support code (intercept.py) by Joshua D. Bartlett

Original Ruby version written by Ian Macdonald <ian@caliban.org>

COPYRIGHT
---------
Copyright (C) 2013 Antti Haapala

Portions Copyright (C) Joshua D. Bartlett

Portions Copyright (C) 2003-2004 Ian Macdonald

This is free software; see the source for copying conditions.
There is NO warranty; not even for MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.

FILES
-----

* /usr/local/etc/acoc.con
* /etc/acoc.conf
* ~/.acoc.conf

ENVIRONMENT
-----------

$ACOCRC
$PEACOCKRC
  If set, this specifies the location of an additional configuration file.

CONTRIBUTING
-------------

peacock is only as good as the configuration file that it uses. If you compose
pattern-matching rules that you think would be useful to other people, please
send them to me for inclusion in a subsequent release.

SEE ALSO
--------

* acoc.conf(5)

BUGS
----

* Nested regular expressions do not work well.
* Inner subexpressions need to use clustering (?:), not capturing (). In other words, they can be used for matching, but not for coloring.
"""

import re
import os
import pty
import sys

from os.path import basename
from collections import defaultdict
from intercept import Interceptor

PROGRAM_PATH = os.path.realpath(__file__)

PROGRAM_NAME = basename(__file__)
PROGRAM_VERSION = '0.1'
DEBUG=False

def myprint(*args, **kwargs):
    file = kwargs.get('file', sys.stdout)
    file.write(' '.join([ str(i) for i in args ]) + '\n')

class Program(object):
    def __init__(self, flags=""):
        self.flags = flags or ""
        self.specs = []

    def compile(self):
        for i in self.specs:
            i.compile()

    def __str__(self):
        return "<program settings>"

    def __repr__(self):
        return "<program settings>"

SECTION_HEAD = re.compile(r'\[(.*)\]')
LINE_REGEX   = re.compile(r'(.)([^\1]*)\1(g?)\s+(.*)')

cmd = defaultdict(Program)

def nopmaker():
    return lambda a: a

ATTRS = dict(
    bright='1',
    bold='1',
    red='1;31',
    green='1;32',
    yellow='1;33',
    blue='1;34',
    magenta='1;35',
    cyan='1;36',
    white='1;37',
    blink='5',
    on_red='41'
)

def get_set(attr):
    rv = ATTRS.get(attr)
    if not rv:
        return ''

    return '\033[%sm' % rv

def get_reset(attr):
    if attr in ATTRS:
        return "\033[0m"

    return ''

class Rule(object):
    def __init__(self, regex, flags, colors):
        self.regex   = regex
        self.flags   = flags
        self.colors = colors
        
        self.color_brackets = defaultdict(nopmaker)
        self.create_brackets()

    def create_brackets(self):
        """
        Create a bracketting function for all numbered groups.
        The defaultdict shall be modified so that the lastly
        defined colorfunc shall be used for all remaining invocations!
        """
        def make_color_bracket(sets, resets):
            return lambda x: sets + x + resets

        for n, i in enumerate(self.colors):
            attrs = i.split('+')
            sets = ''
            resets = ''
            for j in attrs:
                j = j.strip()
                sets += get_set(j)
                resets += get_reset(j)

            if sets:
                # we have some color...
                self.color_brackets[n] = make_color_bracket(sets, resets)

        def last_bracket_maker():
            return make_color_bracket(sets, resets)

        self.color_brackets.default_factory = last_bracket_maker

    def compile(self):
        self.compiled = re.compile(self.regex)

    def do_sub(self, line):
        spans = []
        if self.flags == 'g':
            for match in self.compiled.finditer(line):
                spans.append((match.start(), match.end()))

            if not spans:
                # no matches, no colors, sorry.
                return

        else:
            m = self.compiled.search(line)

            # no matches
            if not m:
                return

            # no matches in subgroups at all, but hey we still matched!
            if not m.lastindex:
                return line

            for i in range(1, m.lastindex + 1):
                spans.append(m.span(i))

        pos = 0
        output = ''
        for i, span in enumerate(spans):
            start, end = span
            if start == -1 or start < pos:
                # we do not handle nested grps, sorry :D
                continue

            output += line[pos:start]
            bracketed = line[start:end]
            output += self.color_brackets[i](bracketed)
            pos = end

        output += line[pos:]
        return output

def debug(msg, *args):
    if not DEBUG:
        return

    myprint(msg % args, file=sys.stderr)

# set things up
#
def initialize():
    config_files = [
        os.path.join(os.path.dirname(PROGRAM_PATH), 'acoc.conf'),
        '/etc/acoc.conf',
        '/usr/local/etc/acoc.conf',
        '~/.acoc.conf',
        os.environ.get('ACOCRC'),
        os.environ.get('PEACOCKRC')
    ]

    if not parse_config(*config_files):
        myprint("No readable config files found.", file=sys.stderr)
        sys.exit(1)

# get configuration data
#
def parse_config(*files):
    parsed = False

    for file in files:
        if not file:
            continue

        file = os.path.expanduser(file)
        if not (os.access(file, os.R_OK) and os.path.isfile(file)):
            continue

        debug("Attempting to read config file: %s", file)

        try:
            with open(file) as f:
                for line in f:
                    line = line.strip()
                    if not line or line[0] == '#':
                        continue

                    m = SECTION_HEAD.match(line)
                    if m:
                        progs = [ i.strip() for i in m.group(1).split(',') ]
                        invs = []
                        for inv in progs:
                            if '/' in inv:
                               inv, flags = inv.split('/', 1)
                            else:
                               flags = ''

                            if 'r' in flags:
                                program = inv.split()[0]
                                for k in list(cmd.keys()):
                                    if k.split()[0] == program:
                                        del cmd[k]

                                flags = flags.replace('r', '')

                            cmd[inv].flags += flags
                            invs.append(inv)

                        continue
                    
                    match = LINE_REGEX.match(line)  
                    if not match:
                        myprint("Ignoring bad config line: %s" % line, file=sys.stderr)
                        continue

                    # numbering 0 based in match.groups!
                    regex, flags, colors = match.groups()[1:4]
                    colors = [ i.strip() for i in colors.split(',') ]
                    for i in invs:
                        cmd[i].specs.append(Rule(regex, flags, colors))

                parsed = True

        except Exception as e:
            debug("Got exception: %s\n", e)

    return parsed

class Colorizer(Interceptor):
    def __init__(self, prog):
        self.prog = prog
        self.prog.compile()
        self.flags = prog.flags
        self.specs = prog.specs
        super(Colorizer, self).__init__()

    def do_process(self, data):
        line_end = ''
        if data.endswith('\n'):
            line_end = '\n'
            if data.endswith('\r\n'):
                line_end = '\r\n'

        lines = data.splitlines(False)
        for i in range(len(lines)):
            for j in self.specs:
                replaced = j.do_sub(lines[i])
                if replaced:
                    lines[i] = replaced
                    break	

        return '\r\n'.join(lines) + line_end

initialize()

argv = sys.argv[1:]
if not argv:
    myprint("Usage: peacock PROGRAM ARGUMENTS...", file=sys.stderr)
    sys.exit(1)

argsjoined = ' '.join(argv)
bestmatch = None
bestlength = 0	
cmdregexes = cmd.keys()

for i in cmdregexes:
    m = re.search('^' + i, argsjoined)
    if m:
        matchlen = len(m.group(0))
        if matchlen > bestlength:
            bestmatch = i
            bestlength = matchlen

if not bestmatch:
    sys.stdout.flush()
    try:
        os.execvp(argv[0], argv)
    except:
        myprint("peacock: command not found: %s" % argv[0], file=sys.stderr)
        sys.exit(1)

rules = cmd[bestmatch]
colorizer = Colorizer(rules)
argv = sys.argv[1:]
colorizer.spawn(argv)
