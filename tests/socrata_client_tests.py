import json
import unittest
import requests
import logging

from app_config import AppConfig
from socrate_api.socrata_client import SocrataClient


class SocrataClientTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = AppConfig()
        self.socrata_client = SocrataClient()

    def test_fetch_all_housing_data_generator_should_return_data(self):
        result_getn = self.socrata_client.fetch_all_housing_data_generator(limit=1000)
        for r in result_getn:
            assert len(r) >0
        assert True

    def test_fetch_csv_data(self):
        data = self.socrata_client.get_housing_data()
        assert len(data)>0

    def test_insert_socrata_data(self):
        raise NotImplementedError()


if __name__ == '__main__':
    unittest.main()
