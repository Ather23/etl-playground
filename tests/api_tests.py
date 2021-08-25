import json
import unittest
import requests

from app_config import AppConfig


class ApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = AppConfig()

    def test_fetch_data_from_scorata(self):
        result = requests.get(self.config.SocrataApiBaseUrl,
                              headers={
                                  'X-App-Token': self.config.SocratSecret,
                              },
                              params={
                                  "$limit": 5,
                                  "$offset": 0,
                                  "$order": "id"
                              })
        result = json.loads(result.content)
        assert len(result) > 0

    def test_pagination(self):
        result = requests.get(self.config.SocrataApiBaseUrl,
                              headers={
                                  'X-App-Token': self.config.SocratSecret,
                              },
                              params={
                                  "$limit": 5,
                                  "$offset": 0,
                                  "$order": "id"
                              })
        result = json.loads(result.content)
        assert len(result) == 5


if __name__ == '__main__':
    unittest.main()
