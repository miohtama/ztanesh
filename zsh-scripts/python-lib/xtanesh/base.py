from __future__ import print_function
import sys
import os
import zipimporter
from struct import pack, unpack
from Xlib import error 

import Xlib
import Xlib.display
from Xlib.xobject.drawable import Window
from Xlib import X, Xatom

class XClientBase(object):
    WM_NAME = 'XtaneSH Server'

    def __init__(self, display_name=None, *a, **kw):
        if display_name is None:
            try:
                display_name = os.environ['DISPLAY']
            except:
                self.error("No DISPLAY specified, quitting!")

        super(XClientBase, self).__init__(*a, **kw)
        self.display = Xlib.display.Display(display_name)
        self.root = self.display.screen().root
        self.XTANESH_WINDOW  = self.display.intern_atom('_XTANESH_WINDOW_ID', only_if_exists=False)
        self.XTANESH_COMMAND = self.display.intern_atom('_XTANESH_COMMAND', only_if_exists=False)
        self.UTF8_STRING = self.display.intern_atom('UTF8_STRING', only_if_exists=False)

    def error(self, code=1, *args):
        print(*args, file=sys.stderr)
        sys.exit(code)

    def set_UTF8_property(self, window, atom, value):
        if not isinstance(value, str):
            value = value.encode('UTF-8')

        return window.change_property(
            atom,
            self.UTF8_STRING,
            8,
            value
        )

    def get_UTF8_property(self, window, atom, delete=False):
        value = window.get_property(
            atom,
            self.UTF8_STRING,
            0,
            65536,
            delete=delete
        )
        if not value:
            return None

        return value.value

    def set_int_property(self, window, atom, type, value):
        window.change_property(
            atom,
            type,
            32,
            self.pack32(value)
        )

    def get_int_property(self, window, atom, type):
        value = window.get_property(
            atom,
            type,
            0,
            1
        )

        if not value:
            return None

        return value.value[0]

    def pack32(self, value):
        return pack('=I', value)

    def unpack32(self, value):
        return unpack('=I', value)

    def id_to_window(self, id):
        cls = self.display.display.get_resource_class('window', Window)
        the_window = cls(self.display.display, id)
        return the_window

    def is_server_running(self):
        try:
            server_hwnd = self.get_int_property(self.root, self.XTANESH_WINDOW, Xatom.WINDOW)
            if not server_hwnd:
                return False

            the_window = self.id_to_window(server_hwnd)
            if the_window.get_wm_name() != self.WM_NAME:
                return False

            self.server_window = the_window

            return True
                
        except error.BadWindow:
            return False

