from dagster import pipeline, solid


@solid
def fetch_data_from_csv():
    return "dagster"


@solid
def hello(context, name):
    context.log.info(f"Hello, {name}!")


@pipeline
def hello_pipeline():
    hello(get_name())