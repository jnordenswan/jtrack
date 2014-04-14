from lib import model, view

conn = None

def node(**kwargs):
    return model.Node(conn, **kwargs)

def new_node(ntype, data, comment, parents, children):
    new = node(ntype=ntype,
               data=data,
               comment=comment,
               parents=parents,
               children=children)
    view.print_subtree(new.get_roots())

class Controller(object):
    def __init__(self, cl_args):
        self.cl_args = cl_args
        self.connection = connect(self.cl_args['<db-file>'])
        self.transact()

    def transact(self):
        if self.cl_args['l']:
            view.print_subtree(self.roots())
        if self.cl_args['n']:
            self.node(ntype=self.cl_args['<type>'],
                      ndata=self.cl_args['<data>'],
                      ncomment=self.cl_args['<comment>'],
                      nparents=(self.cl_args['parent'],))

    def roots(self):
        cur = self.connection.cursor()
        sql = "SELECT id FROM node LEFT OUTER JOIN relation ON node.id = relation.child WHERE relation.child IS NULL"
        rows = cur.execute(sql).fetchall()
        res = []
        for e in rows:
            name = e[0]
            res.append(self.node(name=name))
        cur.close()
        return res

    def node(self, **kwargs):
        return model.Node(self.connection, **kwargs)