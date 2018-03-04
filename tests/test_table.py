import os
import sqlite3

from unittest import TestCase

from db import Database


class TableTest(TestCase):
    def setUp(self):
        # reset db on every test
        if os.path.isfile("norowdb.sqlite"):
            os.remove("norowdb.sqlite")
        self.db = Database()

    def test_create_table(self):
        self.db.create_table("Cats")

    def test_get_tables(self):
        self.db.create_table("Cats")
        tables = self.db.get_tables()
        self.assertEqual(tables, ["Cats"])

    def test_delete_table(self):
        self.db.create_table("Cats")
        self.db.delete_table("Cats")
        tables = self.db.get_tables()
        self.assertEqual(tables, [])

    def test_duplicate_table(self):
        self.db.create_table("Cats")
        with self.assertRaises(sqlite3.OperationalError):
            self.db.create_table("Cats")

    def test_add_column(self):
        self.db.create_table("Cats")
        self.db.add_column("Cats", "name")

    def test_delete_column(self):
        self.db.create_table("Cats")
        self.db.add_column("Cats", "name")
        self.db.add_column("Cats", "age")
        self.db.delete_column("Cats", "name")

    def test_delete_table_column(self):
        self.db.create_table("Cats")
        self.db.add_column("Cats", "name")
        self.db.add_column("Cats", "age")
        self.db.delete_table("Cats")
        # Check table is deleted
        tables = self.db.get_tables()
        self.assertEqual(tables, [])
        # Check columns are removed
        self.db.create_table("Cats")
        columns = self.db.get_columns("Cats")
        self.assertEqual(columns, [])

    def tearDown(self):
        self.db.close()
