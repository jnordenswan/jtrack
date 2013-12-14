class jt_record(object):

    def __init__(self, db_connection, tablename, row_id=None, **kwargs):
        object.__setattr__(self, "conn", db_connection)
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
        keys_str = str(tuple(kwargs.keys()))
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
