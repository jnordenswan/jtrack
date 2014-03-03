from sqlite3 import connect
import time
import calendar

connection = None


def connect_db(file_path):
    global connection
    connection = connect(file_path)
    cur = connection.cursor()
    cur.execute("PRAGMA foreign_keys=ON")
    cur.close()


def close_db():
    global connection
    connection.close()


def get_roots(connection):
    cur = connection.cursor()
    sql = "SELECT id FROM node LEFT OUTER JOIN relation ON node.id = relation.child WHERE relation.child IS NULL"
    rows = cur.execute(sql).fetchall()
    res = []
    for e in rows:
        res.append(Node(connection, e[0]))
    cur.close()
    return res


class Node(object):
    def __init__(self, connection, nid=None, ntype=None, ndata=None, nparents=None, nchildren=None, ncomment=None):
        self.ntypes = ("P", "R", "S", "C")  # Point, Recurrence, Span, Comment
        self.conn = connection
        self.cur = self.conn.cursor()
        self.nid = nid
        self.ntype = ntype
        self.ndata = ndata
        if self.nid:
            self._check_record_exists()
        elif (self.ntype in self.ntypes and ncomment) or (self.ntype == "comment"):
            self._insert_new_record(nparents, nchildren, ncomment)
        else:
            raise Exception("Unrecognised type or missing comment")

    def _check_record_exists(self):
        sql = "SELECT * FROM node WHERE id=?"
        self.cur.execute(sql, [self.nid])
        res = self.cur.fetchall()
        if len(res) == 0:
            raise Exception("No matching node found :(")
        self.ntype = res[0][1]
        self.ndata = res[0][2]

    def _insert_new_record(self, nparents, nchildren, ncomment):
        try:
            creation_time = time.gmtime()
            creation_time = calendar.timegm(creation_time)
            sql = "INSERT INTO node (type, data, creation_time) VALUES (?, ?, ?)"
            self.cur.execute(sql, [self.ntype, self.ndata, creation_time])
            self.nid = self.cur.lastrowid
            self.ndata = self.ndata.split(',')
            if self.ntype is "R":
                ndata = []
                for e in self.ndata:
                    ndata.append(int(e))
                self.ndata = ndata
            sql = "INSERT INTO relation VALUES (?, ?)"
            if nparents:
                for e in nparents:
                    self.cur.execute(sql, [e, self.nid])
            if nchildren:
                for e in nchildren:
                    self.cur.execute(sql, [self.nid, e])
            if self.ntype is not "comment":
                Node(ntype="comment", ndata=ncomment, nparents=[self.nid])
            self.conn.commit()
        except Exception as ex:
            self.conn.rollback()
            print(ex)

    def get_parents(self, ntypes=None):
        return self.get_adjacent("SELECT parent FROM relation WHERE child=?", ntypes)

    def get_children(self, ntypes=None):
        return self.get_adjacent("SELECT child FROM relation WHERE parent=?", ntypes)

    def get_adjacent(self, sql, ntypes=None):
        self.cur.execute(sql, [self.nid])
        res = []
        for e in self.cur.fetchall():
            n = Node(self.conn, e[0])
            if (ntypes is None) or (n.ntype in ntypes):
                res.append(n)
        return res

    def get_first_comment(self):
        comments = self.get_children("C")
        if len(comments) > 0:
            return comments[0].ndata
        else:
            return None

    def delete(self, cascade=True):
        if cascade:
            for e in self.get_children():
                e.delete(True)
        sql = "DELETE FROM node WHERE id=?"
        self.cur.execute(sql, [self.nid])
        self.conn.commit()
        self.cur.close()
        self.nid = self.ntype = self.ndata = self.conn = self.cur = None