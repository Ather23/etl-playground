import json
import requests

from app_config import AppConfig
from circuitbreaker import circuit


class Client:
    """
    This is a api wrapper for Socrata Api
    """

    def __init__(self):
        self._appConfig = AppConfig()
        self._BASE_URL = self.appConfig.BASE_URL

    def _get_headers(self):
        return {'X-App-Token': self.config.SocratSecret},

    @circuit(failure_threshold=5, expected_exception=ConnectionError)
    def fetch_all_housing_data_generator(self, limit=5, offset_step=5):
        offset = 0
        while True:
            result = requests.get(self.config.SocrataApiBaseUrl,
                                  headers=self._get_headers(),
                                  params={
                                      "$limit": limit,
                                      "$offset": offset,
                                      "$order": "id"
                                  })
            offset += offset_step
            yield json.loads(result.content)
            if result.content is None:
                break

    def get_housing_data(self, limit=100):
        """

        :param limit:
        :return:
        """
        result = requests.get(self.config.SocrataApiBaseUrl,
                              data={
                                  "$$app_token": self.config.SocratSecret,
                                  "$limit": limit
                              })
        result = json.loads(result.content)
        return result
