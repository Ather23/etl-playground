import json
import unittest
import requests

from app_config import AppConfig


class DbTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = AppConfig()

    def test_insert_csv_data(self):
        raise NotImplementedError()

    def test_fetch_csv_data(self):
        raise NotImplementedError()

    def test_insert_socrata_data(self):
        raise NotImplementedError()


if __name__ == '__main__':
    unittest.main()
