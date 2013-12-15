from sqlite3 import connect

connection = None

def connect_db(file_path):
    global connection
    connection = connect(file_path)

def close_db():
    connection.close()

class jt_record(object):

    def __init__(self, tablename, row_id=None, **kwargs):
        object.__setattr__(self, "conn", connection)
        object.__setattr__(self, "table", tablename)
        object.__setattr__(self, "id", row_id)
        if self.id: self._check_record_exists()
        else: self._insert_new_record(kwargs)

    def _check_record_exists(self):
        SQL = "SELECT (id) FROM %s WHERE id=?" % self.table
        cur = self.conn.cursor()
        cur.execute(SQL, [self.id])
        qres = cur.fetchall()
        cur.close()
        if len(qres) == 0:
            raise Exception("No matching record found :(")
        elif len(qres) > 1:
            raise Exception("Table %s has %s records with id %s. What do?" %
                            (self.table, str(len(qres)), str(self.id)))

    def _insert_new_record(self, kwargs):
        SQL = "INSERT INTO %s %s VALUES %s"
        keys_str = "('%s')" % "', '".join(kwargs.keys())
        values = tuple(kwargs.values())
        vals_str = "(%s)" % ", ".join(len(values)*("?"))
        SQL = SQL % (self.table, keys_str, vals_str)
        cur = self.conn.cursor()
        cur.execute(SQL, list(values))
        self.conn.commit()
        object.__setattr__(self, "id", cur.lastrowid)
        cur.close()

    def __getattr__(self, col):
        SQL = "SELECT (%s) FROM %s WHERE id=?"
        SQL = SQL % (col, self.table)
        cur = self.conn.cursor()
        cur.execute(SQL, [self.id])
        res = cur.fetchall()[0][0]
        cur.close()
        return res

    def __setattr__(self, col, value):
        SQL = "UPDATE %s SET %s=? WHERE id=?"
        SQL = SQL % (self.table, col)
        cur = self.conn.cursor()
        cur.execute(SQL, [value, self.id])
        self.conn.commit()
        cur.close()

    def __delattr__(self, col):
        self.__setattr__(col, None)

    def delete(self):
        SQL = "DELETE FROM %s WHERE id=?" % self.table
        cur = self.conn.cursor()
        cur.execute(SQL, [self.id])
        self.conn.commit()
        cur.close()

class event(jt_record):

    def __init__(self, row_id=None, **kwargs):
        jt_record.__init__(self, "event", row_id, **kwargs)

    def _get_members(self, col1, col2):
        res = []
        SQL = "SELECT (%s) FROM event_map WHERE %s=?" % (col1, col2)
        cur = self.conn.cursor()
        cur.execute(SQL, [self.id])
        ids = cur.fetchall()
        for e in ids:
            res.append(event(e[0]))
        cur.close()
        return res

    def get_parents(self):
        return self._get_members("parent", "child")

    def get_children(self):
        return self._get_members("child", "parent")

class commitment(jt_record):

    def __init__(self, row_id=None, **kwargs):
        jt_record.__init__(self, "commitment", row_id, **kwargs)

    def get_events(self):
        res = []
        SQL = "SELECT event_id FROM commitment_map WHERE id=?"
        cur = self.conn.cursor()
        cur.execute(SQL, [self.id])
        ids = cur.fetchall()
        for e in ids:
             res.append(event(e[0]))
        cur.close()
        return res




