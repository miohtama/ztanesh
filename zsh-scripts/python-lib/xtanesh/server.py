from threading import Thread
from . import base
from Xlib import X, Xatom
from Xlib.xobject.drawable import Window
from Xlib.error import BadWindow
import sys

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
                X.StructureNotifyMask
            )
        )

        self.window.set_wm_protocols([self.WM_DELETE_WINDOW])
        self.window.set_wm_name(self.WM_NAME)
	self.window.set_wm_icon_name(self.WM_NAME)

        self.set_int_property(
            self.root,
            self.XTANESH_ATOM,
            Xatom.WINDOW,
            self.window.__window__()
        )

    def run(self):
        self.event_loop()

    def event_loop(self):
        while True:
            event = self.display.next_event()

    def cleanup(self):
        try:
            self.display.close()

        except Exception as e:
            pass

def __main__(args):
    server = Server()
    try:
        server.arguments = args
        server.start()
        while True:
            server.join(600)
            if not server.isAlive():
                break

    except KeyboardInterrupt:
        print >> sys.stderr, "Quitting"
    finally:
        server.cleanup()
    
