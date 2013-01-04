from . import base

class Client(base.XClientBase):
    def __init__(self, *a, **kw):
        super(Client, self).__init__(*a, **kw)

    def run(self, arguments):
        atom = self.get_xtanesh_atom(create=False)
        if not atom:
            self.error('ZtaneSH extensions not present')

def __main__(args):
    client = Client()
    client.run(args)

