from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from app_config import AppConfig
from db.config import DbConfig
from db.socrata import sql_queries
from socrate_api.socrata_client import SocrataClient
import os
import sys
import logging

format = "%d%m%Y-%H%M%S"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(
            os.path.normpath('./etl_logs/socrata_data/socrata_job_{}.log'.format(datetime.utcnow().strftime(format)))),
        logging.StreamHandler(sys.stdout)
    ]
)

app_config = AppConfig()
socrata_client = SocrataClient()
db_config = DbConfig("properly_db")

def extract() -> list:
    """
    Extract data from socrata
    :return: pd.DataFrame
    TODO: What is a return type of a gnerator ??
    """
    logging.info("Extracting csv_data..")
    housing_data_gen = socrata_client.fetch_all_housing_data_generator(limit=5)
    for data in housing_data_gen:
        yield data


def transform(data: list) -> dict:
    """
    TODO: Transform data frame into a dictionary
    :return: dict
    """
    transformed_result = []
    # timestamp conversion 2002-06-28T00:00:00.000
    for d in data:
        try:
            d["issue_date"] = convert_to_datetime(d["application_start_date"])
            d["application_start_date"] = convert_to_datetime(d["application_start_date"])

            d["latitude"] = float(d["latitude"])
            d["longitude"] = float(d["longitude"])

            # ##https://stackoverflow.com/questions/5884066/hashing-a-dictionary
            # d["hash"] = hash(frozenset(d.items()))
            transformed_result.append(d)
        except Exception as e:
            logging.error(e)
            continue
    return transformed_result


def convert_to_datetime(date_as_string: str) -> datetime:
    """
    Conver to datetime
    :param date_as_string: "%Y-%m-%dT%H:%M:%S.%f"
    :return:
    """
    return datetime.strptime(date_as_string, "%Y-%m-%dT%H:%M:%S.%f")


def load_data_to_table(data: list) -> None:
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
            # TODO: Upsert using hashes and sprocs
            insert = (
                row["id"],
                row["permit_"],
                row["permit_type"],
                row["review_type"],
                row["application_start_date"],
                row["issue_date"],
                row["processing_time"],
                row["street_number"],
                row["street_direction"],
                row["street_name"],
                row["suffix"],
                row["work_description"],
                row["building_fee_paid"],
                row["zoning_fee_paid"],
                row["other_fee_paid"],
                row["subtotal_paid"],
                row["building_fee_unpaid"],
                row["zoning_fee_unpaid"],
                row["other_fee_unpaid"],
                row["subtotal_unpaid"],
                row["building_fee_waived"],
                row["zoning_fee_waived"],
                row["other_fee_waived"],
                row["subtotal_waived"],
                row["total_fee"],
                row["reported_cost"],
                row["latitude"],
                row["longitude"],
            )
            cursor.execute(sql_queries.INSERT_ROW, insert)
            conn.commit()
        except Exception as e:
            logging.error(e)
            continue

    cursor.close()


def start_pipeline():
    logging.info("Strating API pipelines")

    for data in extract():
        try:
            t_data = transform(data)
            load_data_to_table(t_data)
        except Exception as e:
            logging.error(e)
            continue
    logging.info("Loading finished for api..")


if __name__ == "__main__":

    logging.info("CHECKPOINT starting csv job")
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
