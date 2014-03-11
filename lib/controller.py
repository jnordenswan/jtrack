from sqlite3 import connect
from lib import model


class Controller(object):
    def __init__(self, db_path):
        self.connection = connect(db_path)

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
        return model.Node(self.connection, kwargs)