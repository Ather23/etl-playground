import mysql.connector


class DbConfig:
    """
    TODO: read from configuration or env variables
    """

    def __init__(self,database):
        self.Host = "172.20.80.1"
        self.UserName = "user"
        self.Password = "password"
        self.Database = database
        self.MysqlConnctor = self.mysq_connector()

    def mysq_connector(self):
        mydb = mysql.connector.connect(
            host=self.Host,
            user=self.UserName,
            password=self.Password,
            database=self.Database
        )

        return mydb
