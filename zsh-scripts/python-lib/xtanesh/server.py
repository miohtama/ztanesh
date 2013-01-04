from . import base

class Server(base.XClientBase):
    def __init__(self, *a, **kw):
        super(Server, self).__init__(*a, **kw)

    def run(self, arguments):
        atom = self.get_xtanesh_atom(create=False)
        if atom:
            self.error('ZtaneSH extensions already running on this X server')

def __main__(args):
    server = Server()
    server.run(args)
