from . import base

class Client(base.XClientBase):
    def __init__(self, *a, **kw):
        super(Client, self).__init__(*a, **kw)
        self.XTANESH_ATOM = self.get_xtanesh_atom(create=True)

    def run(self, arguments):
        if not self.is_server_running():
            self.error('ZtaneSH extensions not present')

def __main__(args):
    client = Client()
    client.run(args)

