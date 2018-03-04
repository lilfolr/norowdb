import sqlite3




# No sql injection checking, but its not like this'll get use in any real environment anyway...

class Database:
    def __init__(self, db_name="norowdb.sqlite"):
        self._tracking_tbl = 'tables'
        self.conn = sqlite3.connect(db_name)
        self._run_none_sql(f"CREATE TABLE `{self._tracking_tbl}` (`{self._tracking_tbl}`	TEXT)")

    @staticmethod
    def _drop_column_sql(table_name, new_columns):
        return f"""
        BEGIN TRANSACTION;
        CREATE TEMPORARY TABLE {table_name}_backup({new_columns});
        INSERT INTO {table_name}_backup SELECT {new_columns} FROM {table_name};
        DROP TABLE {table_name};
        CREATE TABLE {table_name}({new_columns});
        INSERT INTO {table_name} SELECT {new_columns} FROM {table_name}_backup;
        DROP TABLE {table_name}_backup;
        COMMIT;
        """

    def create_table(self, table_name):
        if "_" in table_name:
            raise DBException("_ can't appear in table names")
        self._run_none_sql(f"CREATE TABLE {table_name}({table_name})")
        self._run_none_sql(f"ALTER TABLE {self._tracking_tbl} ADD COLUMN {table_name}")

    def get_tables(self):
        x = self._run_all_sql("SELECT tbl_name FROM sqlite_master WHERE type=='table'")
        return [a[0] for a in x if not a[0] == 'tables' and "_" not in a[0]]

    def delete_table(self, table_name):
        for column in self.get_columns(table_name):
            self.delete_column(table_name, column)
        self._run_none_sql(f"DROP TABLE {table_name}")
        new_cols = self.get_columns(self._tracking_tbl, True)
        new_cols.remove(table_name)
        new_columns = ",".join(new_cols)
        drop_column_sql = self._drop_column_sql(self._tracking_tbl, new_columns)
        self._run_none_sqls(drop_column_sql)

    def add_column(self, table_name, column_name):
        column_table = f"{table_name}_{column_name}"
        self._run_none_sql(f"CREATE TABLE {column_table}(`values` TEXT)")
        self._run_none_sql(f"ALTER TABLE {table_name} ADD COLUMN {column_table}")

    def get_columns(self, table_name, include_self=False):
        x = self._run_all_sql(f"PRAGMA table_info({table_name})")
        return [a[1].replace(f"{table_name}_","") for a in x if a[1] != table_name or include_self]

    def delete_column(self, table_name, column_name):
        column_table = f"{table_name}_{column_name}"
        self._run_none_sql(f"DROP TABLE {column_table}")
        new_cols = self.get_columns(table_name, True)
        new_cols.remove(column_name)
        new_cols_formatted = []
        for c in new_cols:
            new_cols_formatted.append(table_name+"_"+c if c!=table_name else c)
        new_columns = ",".join(new_cols_formatted)

        drop_column_sql = self._drop_column_sql(table_name, new_columns)
        self._run_none_sqls(drop_column_sql)

    def close(self):
        self.conn.close()

    def _run_none_sql(self, sql):
        self.conn.execute(sql)
        self.conn.commit()

    def _run_all_sql(self, sql):
        c = self.conn.cursor()
        c.execute(sql)
        return c.fetchall()

    def _run_none_sqls(self, sql):
        self.conn.executescript(sql)


class DBException(Exception):
    pass
