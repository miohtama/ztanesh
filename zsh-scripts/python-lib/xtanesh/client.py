from . import base

import json

class Client(base.XClientBase):
    def __init__(self, *a, **kw):
        super(Client, self).__init__(*a, **kw)
        self.server_window = None

    def run(self, arguments):
        if not self.is_server_running():
            self.error('ZtaneSH extensions not present')

        self.send_command({'foo': 'bar'})

    def send_command(self, data):
        serialized = json.dumps(data)
        self.set_UTF8_property(
                self.server_window,
                self.XTANESH_COMMAND,
                serialized
        )
        self.display.flush()

def __main__(args):
    client = Client()
    client.run(args)

