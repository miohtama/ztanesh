from threading import Thread
from . import base
from Xlib import X, Xatom
from Xlib.xobject.drawable import Window
from Xlib.error import BadWindow
import sys
import json

class Server(base.XClientBase, Thread):
    def __init__(self, *a, **kw):
        super(Server, self).__init__(*a, **kw)

        self.daemon = True

 	self.WM_DELETE_WINDOW = self.display.intern_atom('WM_DELETE_WINDOW')
	self.WM_PROTOCOLS = self.display.intern_atom('WM_PROTOCOLS')

        self.screen = self.display.screen()

        if self.is_server_running():
            self.error("A XtaneSH instance is already running on this display")

        self.create_window()

    def create_window(self):
        self.window = self.root.create_window(
            100, 100, 400, 300, 0,
            self.screen.root_depth,
            X.InputOutput,
            X.CopyFromParent,
            event_mask=(
                X.StructureNotifyMask |
                X.PropertyChangeMask  
            )
        )

        self.window.set_wm_protocols([self.WM_DELETE_WINDOW])
        self.window.set_wm_name(self.WM_NAME)
	self.window.set_wm_icon_name(self.WM_NAME)
        self.set_int_property(
            self.root,
            self.XTANESH_WINDOW,
            Xatom.WINDOW,
            self.window.__window__()
        )

    def run(self):
        self.event_loop()

    def event_loop(self):
        self.display.flush()
        while True:
            e = self.display.next_event()

            # Window has been destroyed, quit
            if e.type == X.DestroyNotify:
                sys.exit(0)

            # Somebody wants to tell us something
            elif e.type == X.ClientMessage:
                if e.client_type == self.WM_PROTOCOLS:
                    fmt, data = e.data
                    if fmt == 32 and data and data[0] == self.WM_DELETE_WINDOW:
                        sys.exit(0)

            elif e.type == X.PropertyNotify and e.atom == self.XTANESH_COMMAND:
                command_string = self.get_UTF8_property(
                    self.window, self.XTANESH_COMMAND
                )
                if command_string:
                    self.process_command(command_string)

    def process_command(self, command_string):
        try:
            command = json.loads(command_string)
	    print >> sys.stderr, "Received a command: %s" % command

        except Exception as e:
            print >> sys.stderr, "Got an exception when parsing command: %s, %s" % (e.__class__.__name__, e)

    def cleanup(self):
        try:
            self.display.close()

        except Exception as e:
            pass

def __main__(args):
    server = Server()
    server.run()
    server.cleanup()
    sys.exit(0)
