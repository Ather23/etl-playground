import sys
from datetime import datetime
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler

from app_config import AppConfig
from db.config import DbConfig
from db.csv_data import sql_queries
import os

# TODO: Log to cloud watch/azure monitor
# May be a custom logging framework ??
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(
            os.path.normpath('./etl_logs/csv_data/csv_job_{}.log'.format(
                datetime.utcnow().strftime("%d%m%Y-%H%M%S")))),
        logging.StreamHandler(sys.stdout)
    ]
)

app_config = AppConfig()
db_config = DbConfig("properly_db")

def extract() -> pd.DataFrame:
    """
    Extract data from csv_data
    :return: pd.DataFrame
    """
    logging.info("Extracting csv_data..")
    return pd.read_csv(app_config.CsvPath)


def transform(data: pd.DataFrame) -> dict:
    """
    TODO: Transform data frame into a dictionary
    :return: dict
    """
    # timestamp conversion
    data["date"] = pd.to_datetime(data["date"],
                                  format="%Y-%m-%d %H:%M:%S"). \
        dt.strftime("%Y-%m-%d %H:%M:%S")
    df_dict = data.to_dict('records')
    return df_dict


def load_data_to_table(data: dict) -> None:
    """
    Insert data to mysql db
    :return:None
    """

    logging.info("Loading data..")

    # TODO:Move this out of this function
    conn = db_config.MysqlConnctor
    cursor = conn.cursor()

    for row in data:
        try:
            ##TODO: Upsert using hashes and sprocs
            insert = (
                row["id"],
                row["date"],
                row["price"],
                row["bedrooms"],
                row["bathrooms"],
                row["sqft_living"],
                row["sqft_lot"],
                row["view"],
                row["condition"],
                row["grade"],
                row["sqft_above"],
                row["yr_built"],
                row["yr_renovated"],
                row["zipcode"],
                row["lat"],
                row["long"],
                row["sqft_living15"],
                row["sqft_lot15"]
            )
            cursor.execute(sql_queries.INSERT_ROW, insert)
            conn.commit()
        except Exception as e:
            logging.error(e)
            continue
    logging.info("Loading finished..")
    cursor.close()


def start_pipeline():
    logging.info("Strating csv pipelines")
    load_data_to_table(transform(extract()))


if __name__ == "__main__":
    logging.info("CHECKPOINT starting api job")

    conn = db_config.MysqlConnctor
    cursor = conn.cursor()
    cursor.execute(sql_queries.CREATE_DB)
    cursor.execute(sql_queries.DROP_TABLE_QUERY)
    cursor.execute(sql_queries.CREATE_TABLE_QUERY)
    conn.commit()

    sched = BackgroundScheduler(daemon=True)

    try:
        sched.add_job(start_pipeline(), 'interval', hour=1)
    except Exception as e:
        logging.error(e)

