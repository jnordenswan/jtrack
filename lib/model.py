import time
import calendar


class Node(object):
    def __init__(self, connection, **kwargs):
        # Set up tools
        self.ntypes = ("P", "R", "S", "C")  # Point, Recurrence, Span, Comment
        self.conn = connection
        self.cur = self.conn.cursor()

        # Instance variables
        self.name = None
        self.ntype = None
        self.data = None
        self.routine = None

        # Convenience function for evaluating the kwargs validity
        check_kw = lambda name: name in kwargs.keys() and kwargs[name] is not None

        # Logic switchyard
        if check_kw('name'):  # We want to reference an existing node
            self.mirror_db_node(kwargs['name'])
        elif check_kw('ntype') and kwargs['ntype'] in self.ntypes and check_kw('data'):  # New node, check premise
            # Set relatives params to sane values
            ntype = parents = children = None
            if check_kw('ntype'):
                ntype = kwargs['ntype']
            if check_kw('parents'):
                parents = kwargs['parents']
            if check_kw('children'):
                children = kwargs['children']
            if check_kw('routine'):
                routine = kwargs['routine']
            if ntype in ("P", "R", "S") and check_kw('comment'):  # We want to create a point, recurrence, or span
                self.insert_db_node(ntype, kwargs['data'], parents, children, kwargs['comment'], routine)
            elif ntype is "C" and parents:  # We want to create a comment
                self.insert_db_node(ntype, kwargs['data'], parents, None, None)
            else:  # We should never end up here
                raise Exception("We should never end up here")
        else:  # kwargs are bad :(
            raise Exception("kwargs are bad :(")

    def mirror_db_node(self, name):
        sql = "SELECT * FROM node WHERE id=?"
        self.cur.execute(sql, [name])
        res = self.cur.fetchall()
        if len(res) == 0:
            raise Exception("No matching node found in db :(")
        self.name = res[0][0]
        self.ntype = res[0][1]
        self.data = res[0][2]
        self.routine = bool(res[0][3])

    def insert_db_node(self, ntype, data, parents, children, comment, routine):
        try:
            sql = "INSERT INTO node (type, data, creation_time) VALUES (?, ?, ?)"
            self.cur.execute(sql, [ntype, data, routine])
            self.name = self.cur.lastrowid
            self.ntype = ntype
            self.data = data
            self.routine = routine
            if self.ntype is "R":
                data = []
                for e in self.data.split(','):
                    data.append(int(e))
                self.data = data
            sql = "INSERT INTO relation VALUES (?, ?)"
            if parents:
                for e in parents:
                    self.cur.execute(sql, [e, self.name])
            if children:
                for e in children:
                    self.cur.execute(sql, [self.name, e])
            if self.ntype is not "C":
                Node(self.conn, ntype="C", data=comment, parents=[self.name])
            self.conn.commit()
        except Exception as ex:
            self.conn.rollback()
            self.name = self.ntype = self.data = self.conn = self.cur = None
            print(ex)

    def get_parents(self, ntypes=None):
        return self.get_adjacent("SELECT parent FROM relation WHERE child=?", ntypes)

    def get_children(self, ntypes=None):
        return self.get_adjacent("SELECT child FROM relation WHERE parent=?", ntypes)

    def get_adjacent(self, sql, ntypes=None):
        self.cur.execute(sql, [self.name])
        res = []
        for e in self.cur.fetchall():
            n = Node(self.conn, name=e[0])
            if (ntypes is None) or (n.ntype in ntypes):
                res.append(n)
        return res

    def get_first_comment(self):
        comments = self.get_children("C")
        if len(comments) > 0:
            return comments[0].data
        else:
            return None

    def delete(self, cascade=True):
        if cascade:
            for e in self.get_children():
                e.delete(True)
        sql = "DELETE FROM node WHERE id=?"
        self.cur.execute(sql, [self.name])
        self.conn.commit()
        self.cur.close()
        self.name = self.ntype = self.data = self.conn = self.cur = None

    def is_root(self):
        return len(self.get_parents()) is 0

    def is_leaf(self, consider_comments=False):
        if consider_comments:
            res = len(self.get_children()) is 0
        else:
            res = len(self.get_children(ntypes="PRS")) is 0
        return res

    def get_roots(self):
        res = []
        if self.is_root():
            res = [self]
        else:
            for e in self.get_parents():
                if e.is_root():
                    res.append(e)
                else:
                    return e.get_roots()
        return res

    def get_recurrences(self):
        res = []
        if self.ntype is 'R':
            res += [self]
        for n in self.get_parents():
            res += n.get_recurrences()
        return res

    def get_leaves(self):
        res = []
        if self.is_leaf():
            res = [self]
        else:
            for n in self.get_children(ntypes='PRS'):
                res += n.get_leaves()
        return res

    def get_commitlets(self):
        pass


class Commitment(object):
    pass


class Commitlet(object):
    pass