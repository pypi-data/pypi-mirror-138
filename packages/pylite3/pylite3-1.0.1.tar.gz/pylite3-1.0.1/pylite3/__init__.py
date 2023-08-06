import sqlite3

class Database(object):
    def __init__(self, file_name):
        self._file_name = file_name

    def connect(self):
        self._con = sqlite3.connect(self._file_name)
        self._cur = self._con.cursor()

        return self

    def close(self):
        self._con.close()
        return self

    @property
    def result(self):
        return self._result

    def select(self, table_name, item=None, where=None, values=()):
        query = f"SELECT {'*' if item is None else item}" \
                    f" FROM {table_name}"

        if where:
            query += f" WHERE {where}"

        self._cur.execute(query, values if len(values) else values)
        self._result = self._cur.fetchall()

        return self

    def insert(self, table_name, params, values):
        temp = ''
        for _ in range(len(values)):
            temp += '?, '

        self._cur.execute(f"INSERT INTO {table_name}({params})" \
                                f" VALUES ({temp[:-2]})", values)
        self._con.commit()

        return self

    def update(self, table_name, params, where, values):
        self._cur.execute(f"UPDATE {table_name}" \
                                f" SET {params}" \
                                f" WHERE {where}", values)
        self._con.commit()

        return self

    def delete(self, table_name, where, values):
        self._cur.execute(f"DELETE FROM {table_name}" \
                                f" WHERE {where}", values)
        self._con.commit()

        return self