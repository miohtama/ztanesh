#!/usr/bin/env python
from __future__ import print_function

import os
import sys
import glob

libdir = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    'eggs'
))

eggs = [ os.path.join(libdir, i) for i in os.listdir(libdir)
    if i[-4:] in [ '.egg', '.zip' ] ]

sys.path.extend(eggs)
