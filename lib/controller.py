from lib import model, view, util

conn = None

def node(**kwargs):
    return model.Node(conn, **kwargs)

def new_node(ntype, data, comment, parents, children, routine):
    new = node(ntype=ntype,
               data=data,
               comment=comment,
               parents=parents,
               children=children,
               routine=routine)
    view.print_subtree(new.get_roots())

def view_node(name):
    n = node(name=util.str_to_int(name))
    roots = n.get_roots()
    view.print_subtree(roots)

def delete_node(name):
    n = node(name=util.str_to_int(name))
    n.delete()

def get_roots():
    cur = conn.cursor()
    sql = "SELECT id FROM node LEFT OUTER JOIN relation ON node.id = relation.child WHERE relation.child IS NULL"
    rows = cur.execute(sql).fetchall()
    res = []
    for e in rows:
        name = e[0]
        res.append(node(name=name))
    cur.close()
    return res

def get_span(start, end=None):
    if not end:
        end = start + (60 * 60 * 24)
    cur = conn.cursor()
    sql = "SELECT * FROM node WHERE type=\"P\" AND DATA BETWEEN ? AND ?"
    cur.execute(sql, [start, end])
    res = cur.fetchall()
    cur.close()
    return res

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