import unittest
from datetime import datetime

from app_config import AppConfig
from socrate_api.socrata_client import SocrataClient


class SocrataClientTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = AppConfig()
        self.socrata_client = SocrataClient()

    def test_fetch_all_housing_data_generator_should_return_data(self):
        result_getn = self.socrata_client.fetch_all_housing_data_generator(limit=1000)
        for r in result_getn:
            assert len(r) > 0
        assert True

    def test_fetch_csv_data(self):
        data = self.socrata_client.get_housing_data()
        assert len(data) > 0

    def test_insert_socrata_data(self):
        raise NotImplementedError()

    def test_application_start_data_conversion(self):
        """
        Should convert to formatted datetime
        :return:
        """
        test_date = "2002-06-28T00:00:00.000"
        conv_date = datetime.strptime(test_date, "%Y-%m-%dT%H:%M:%S.%f")

        assert conv_date.date().year == 2002
        assert conv_date.date().month == 6
        assert conv_date.date().day == 28


if __name__ == '__main__':
    unittest.main()
