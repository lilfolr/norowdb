import sqlite3


# No sql injection checking, but its not like this'll get use in any real environment anyway...

class Database:
    def __init__(self, db_name="norowdb.sqlite"):
        self._tracking_tbl = 'tables'
        self.conn = sqlite3.connect(db_name)
        self._run_none_sql(f"CREATE TABLE `{self._tracking_tbl}` (`{self._tracking_tbl}`	TEXT)")

    def create_table(self, table_name):
        if "_" in table_name:
            raise DBException("_ can't appear in table names")
        self._run_none_sql(f"CREATE TABLE {table_name}({table_name})")
        self._run_none_sql(f"ALTER TABLE {self._tracking_tbl} ADD COLUMN {table_name}")

    def get_tables(self):
        x = self._run_all_sql("SELECT tbl_name FROM sqlite_master WHERE type=='table'")
        return [a[0] for a in x if not a[0] == 'tables' and "_" not in a[0]]

    def add_column(self, table_name, column_name):
        column_table = f"{table_name}_{column_name}"
        self._run_none_sql(f"CREATE TABLE {column_table}(`values` TEXT)")
        self._run_none_sql(f"ALTER TABLE {table_name} ADD COLUMN {column_table}")

    def close(self):
        self.conn.close()

    def _run_none_sql(self, sql):
        self.conn.execute(sql)
        self.conn.commit()

    def _run_all_sql(self, sql):
        c = self.conn.cursor()
        c.execute(sql)
        return c.fetchall()


class DBException(Exception):
    pass
