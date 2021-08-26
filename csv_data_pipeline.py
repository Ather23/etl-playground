from dagster import pipeline, solid

import pandas as pd

from app_config import AppConfig


@solid
def fetch_data_from_csv():
    app_config =AppConfig()
    df = pd.read_csv(app_config.CsvPath)

    return "dagster"


@solid
def hello(context, name):
    context.log.info(f"Hello, {name}!")


@pipeline
def hello_pipeline():
    hello()