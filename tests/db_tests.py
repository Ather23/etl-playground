import json
import unittest
import requests

from app_config import AppConfig
from db.config import DbConfig
from db.csv_data import sql_queries


class DbTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = AppConfig()
        self.db_config = DbConfig("properly_db")

    def test_create_csv_table_should_create_table(self):
        conn = self.db_config.MysqlConnctor
        cursor =conn.cursor()
        cursor.execute(sql_queries.CREATE_TABLE_QUERY)
        conn.commit()
        cursor.close()


    def test_insert_csv_data(self):
        raise NotImplementedError()

    def test_fetch_csv_data(self):
        raise NotImplementedError()

    def test_insert_socrata_data(self):
        raise NotImplementedError()


if __name__ == '__main__':
    unittest.main()
