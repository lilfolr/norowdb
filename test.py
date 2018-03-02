import os
import sqlite3

from unittest import TestCase

from db import Database


class TableTest(TestCase):
    def setUp(self):
        # reset db on every test
        try:
            os.remove("/home/lilfolr/Documents/Personal/Projects/norowdb/norowdb.sqlite")
        except:
            pass
        self.db = Database()

    def test_create_table(self):
        self.db.create_table("Cats")

    def test_get_tables(self):
        self.db.create_table("Cats")
        tables = self.db.get_tables()
        self.assertEqual(tables, ["Cats"])

    def test_duplicate_table(self):
        self.db.create_table("Cats")
        with self.assertRaises(sqlite3.OperationalError):
            self.db.create_table("Cats")

    def test_add_column(self):
        self.db.create_table("Cats")
        self.db.add_column("Cats", "name")

    def tearDown(self):
        self.db.close()
