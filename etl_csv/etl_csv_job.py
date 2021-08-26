import pandas as pd
from app_config import AppConfig
import logging
from db.config import DbConfig
from db.csv_data import sql_queries
from datetime import datetime

app_config = AppConfig()


def extract() -> pd.DataFrame:
    logging.info("Extracting csv..")
    return pd.read_csv(app_config.CsvPath)


def transform(data: pd.DataFrame) -> dict:
    """
    TODO:
    :return:
    """
    #timestamp conversion
    data["date"] = pd.to_datetime(data["date"], format="%Y-%m-%d %H:%M:%S").dt.strftime("%Y-%m-%d %H:%M:%S")
    df_dict = data.to_dict('records')
    return df_dict


def load(data: dict) -> None:
    """

    :return:
    """

    logging.info("Loading data..")

    # TODO:Move this out of this function
    db_config = DbConfig("properly_db")
    conn = db_config.MysqlConnctor
    cursor = conn.cursor()
    cursor.execute("DROP TABLE kaggle_data")
    cursor.execute(sql_queries.CREATE_TABLE_QUERY)
    conn.commit()

    for row in data:
        try:
            insert =(
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
    logging.info("Loading finished..s")
    cursor.close()

if __name__ == "__main__":
    load(transform(extract()))
