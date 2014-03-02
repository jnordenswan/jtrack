from sqlite3 import connect
import time
import calendar

connection = None

def connect_db(file_path):
    global connection
    connection = connect(file_path)

def close_db():
    connection.close()

class Node(object):
    def __init__(self, nid=None, ntype=None, ndata=None, nparents=None, nchildren=None):
        types = ("point", "recurrence", "span", "comment")
        self.conn = connection
        self.cur = self.conn.cursor()
        self.nid = nid
        self.ntype = ntype
        self.ndata = ndata
        if self.nid:
            self._check_record_exists()
        elif self.ntype in types:
            self._insert_new_record(nparents, nchildren)
        else:
            raise Exception("Unrecognised type")

    def _check_record_exists(self):
        SQL = "SELECT (id) FROM node WHERE id=?"
        self.cur.execute(SQL, [self.nid])
        res = self.cur.fetchall()
        if len(res) == 0:
            raise Exception("No matching record found :(")

    def _insert_new_record(self, nparents, nchildren):
        creation_time = time.gmtime()
        creation_time = calendar.timegm(creation_time)
        self.cur.execute("INSERT INTO node VALUES ? ? ?", [self.ntype, self.ndata, creation_time])
        self.nid = self.cur.lastrowid
        sql = "INSERT INTO relation VALUES (?,?)"
        for e in nparents:
            self.cur.execute(sql, [e, self.nid])
        for e in nchildren:
            self.cur.execute(sql, [self.nid, e])
        self.conn.commit()

    def get_adjacent(self, sql):
        self.cur.execute(sql, [self.nid])
        res = []
        for e in self.cur.fetchall():
            res.append(Node(e[0], e[1]))
        return res

    def get_parents(self):
        return self.get_adjacent("SELECT parent FROM relation WHERE child=?")

    def get_children(self):
        return self.get_adjacent("SELECT child FROM relation WHERE parent=?")

    def delete(self, cascade):
        sql = "DELETE FROM node WHERE id=?"
        self.cur.execute(sql, [self.nid])
        self.conn.commit()
        self.cur.close()
        self.nid = self.ntype = self.ndata = self.conn = self.cur = None