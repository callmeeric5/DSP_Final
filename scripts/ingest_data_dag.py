from pendulum import today
from datetime import timedelta
from airflow.decorators import dag, task
import pandas as pd
from great_expectation import validate_data, send_teams_alert
from save_log import save_data_logs
import os
import random

from _scproxy import _get_proxy_settings

_get_proxy_settings()
os.environ["NO_PROXY"] = "*"


@dag(
    dag_id="ingest_data",
    description="Ingest data",
    tags=["data-quality files"],
    default_args={"owner": "airflow"},
    schedule=timedelta(minutes=5),
    start_date=today().add(hours=-1),
    dagrun_timeout=timedelta(minutes=20),
)
def ingest_data():
    @task
    def get_ingestion_data():
        print("The get_ingestion_data is running")
        return _get_ingestion_data()

    @task
    def validate_data_gx(df):
        print("The validate_data_gx is running")
        report = validate_data(df)

        return report

    @task
    def send_alert(error):
        if error:
            send_teams_alert(error)
        else:
            print("No data validation errors. Skipping alert.")

    @task
    def save_data_errors(validation_results):
        save_data_logs(validation_results)
        print("Save data errors to database:")

    data_to_ingest = get_ingestion_data()

    errors = validate_data_gx(data_to_ingest)
    send_alert(errors)
    save_data_errors(errors)


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
    print("_get_ingestion_data is running")
    return df


ingest_data_dag = ingest_data()
