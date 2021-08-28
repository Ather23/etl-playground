

class AppConfig:
    """

    TODO: read from configuration or env variables
    """
    def __init__(self):
        self.SocrataApiBaseUrl = "https://data.cityofchicago.org/resource/ydr8-5enu.json"
        self.SocratSecret = ""
        self.CsvPath ="./data/kc_house_data.csv"