# from pendulum import today
#
#
# from datetime import timedelta
# from airflow.decorators import dag, task
# import pandas as pd
# from great_expectation import validate_data, send_teams_alert
# import os
# import random
# import logging
#
# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# print("Current working directory:", os.getcwd())
#
#
# @dag(
#     dag_id="ingest_data",
#     description="Ingest data",
#     tags=["data-quality files"],
#     default_args={"owner": "airflow"},
#     schedule=timedelta(minutes=2),
#     start_date=today().add(hours=-1),
#     dagrun_timeout=timedelta(minutes=1),
# )
# def ingest_data():
#     @task
#     def get_ingestion_data():
#         return _get_ingestion_data()
#
#     @task
#     def validate_data_gx(df):
#         try:
#             errors = validate_data(df)
#             errors = [str(error) for error in errors]
#             return errors
#         except Exception as e:
#             logger.error(f"Error occurred during data validation: {e}")
#             return [f"Error occurred during data validation: {e}"]
#
#     @task
#     def send_alert(errors):
#         if errors:
#             send_teams_alert(errors)
#         else:
#             logger.info("No data validation errors. Skipping alert.")
#
#     data_to_ingest = get_ingestion_data()
#     errors = validate_data_gx(data_to_ingest)
#     send_alert(errors)
#
#
# def _get_ingestion_data():
#     ingestion_folder = "/Users/ericwindsor/Documents/EPITA_ERIC/Data_Scicence_Production/DSP_Final/data_raw/Ingestion"
#     files = os.listdir(ingestion_folder)
#     if not files:
#         logger.error("No files found in the ingestion folder.")
#         return pd.DataFrame()
#     selected_file = random.choice(files)
#     file_path = os.path.join(ingestion_folder, selected_file)
#     df = pd.read_csv(file_path)
#     os.remove(file_path)
#     return df
#
#
# ingest_data_dag = ingest_data()

from pendulum import today
from datetime import timedelta
from airflow.decorators import dag, task
import pandas as pd
from great_expectation import validate_data, send_teams_alert
import os
import random
from great_expectations.core.batch import RuntimeBatchRequest
from datetime import datetime
import requests

@dag(
    dag_id="ingest_data",
    description="Ingest data",
    tags=["data-quality files"],
    default_args={"owner": "airflow"},
    schedule=timedelta(minutes=2),
    start_date=today().add(hours=-1),
    dagrun_timeout=timedelta(minutes=1),
)
def ingest_data():
    @task
    def get_ingestion_data():
        return _get_ingestion_data()

    @task
    def validate_data_gx(df):
        try:
            errors = validate_data(df)
            errors = [str(error) for error in errors]
            return errors
        except Exception as e:
            return [f"Error occurred during data validation: {e}"]

    @task
    def send_alert(errors):
        if errors:
            send_teams_alert(errors)
        else:
            print("No data validation errors. Skipping alert.")

    data_to_ingest = get_ingestion_data()
    errors = validate_data_gx(data_to_ingest)
    send_alert(errors)


def _get_ingestion_data():
    ingestion_folder = "/Users/ericwindsor/Documents/EPITA_ERIC/Data_Scicence_Production/DSP_Final/data_raw/Ingestion"
    files = os.listdir(ingestion_folder)
    if not files:
        print("No files found in the ingestion folder.")
        return pd.DataFrame()
    selected_file = random.choice(files)
    file_path = os.path.join(ingestion_folder, selected_file)
    df = pd.read_csv(file_path)
    os.remove(file_path)
    return df


ingest_data_dag = ingest_data()
