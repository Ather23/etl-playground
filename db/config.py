import mysql.connector
import os
class DbConfig:
    """
    TODO: read from configuration or env variables
    """

    def __init__(self,database):
        #TODO: Read from config instead
        self.Host = 'mysql_db'
        self.UserName = os.environ['MYSQL_USER']
        self.Password = os.environ['MYSQL_PASSWORD']
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
