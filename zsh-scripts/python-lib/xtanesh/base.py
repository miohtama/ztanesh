from __future__ import print_function
import sys
import os
import zipimporter

import Xlib
import Xlib.display
from Xlib import X

class XClientBase(object):
    def __init__(self, display_name=None, *a, **kw):
        if display_name is None:
            try:
                display_name = os.environ['DISPLAY']
            except:
                self.error("No DISPLAY specified, quitting!")

        super(XClientBase, self).__init__(*a, **kw)
        self.display = Xlib.display.Display(display_name)
        self.root = self.display.screen().root

    def error(self, code=1, *args):
        print(*args, file=sys.stderr)
        sys.exit(code)

    def get_xtanesh_atom(self, create=False):
        return self.display.intern_atom('_ZTANESH_WINDOW_ID', only_if_exists=not create)
