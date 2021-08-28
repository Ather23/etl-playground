import json
import requests
from app_config import AppConfig
from circuitbreaker import circuit


class SocrataClient:
    """
    This is a api wrapper for Socrata Api
    TODO: Remove App config dependency
    """

    def __init__(self):
        self._appConfig = AppConfig()
        self._BASE_URL = self._appConfig.SocrataApiBaseUrl

    def _get_headers(self):
        return {'X-App-Token': self._appConfig.SocratSecret}

    @circuit(failure_threshold=5, expected_exception=ConnectionError)
    def fetch_all_housing_data_generator(self, limit=5, offset_step=5):
        """
        Fetches data from api as a generator
        TODO: Fix circuit breaker and test
        TODO: Check if while loop breaks
        :param limit: number of results to fetch
        :param offset_step: next offset
        :return:
        """
        offset = 0
        while True:
            try:
                result = requests.get(self._BASE_URL,
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
            except Exception as e:
                continue

    def get_housing_data(self, limit=100):
        """
        Fetch data based on limit
        :param limit: number of results
        :return:
        """
        result = requests.get(self._BASE_URL,
                              headers=self._get_headers(),
                              data={
                                  "$$app_token": self._appConfig.SocratSecret,
                                  "$limit": limit
                              })
        result = json.loads(result.content)
        return result
