from airflow.exceptions import AirflowSkipException
from pendulum import today
from datetime import timedelta
from airflow.decorators import dag, task
from __init__ import GOOD_DATA_FOLDER
import os
from _scproxy import _get_proxy_settings
import pandas as pd
from inference import predict
from save_to_db import create_prediction_table
from airflow.models import Variable

_get_proxy_settings()
os.environ["NO_PROXY"] = "*"


# GOOD_DATA_FOLDER = ("/Users/ericwindsor"
#                     "/Documents/EPITA_ERIC/Data_Scicence_Production"
#                     "/DSP_Final/data_raw/split_data/Clean_Data")

@dag(
    dag_id="predict_data",
    description="Predict data",
    tags=["prediction"],
    default_args={"owner": "airflow"},
    schedule=timedelta(minutes=2),
    start_date=today().add(hours=-1),
    dagrun_timeout=timedelta(minutes=20),
)
def predict_data():
    @task
    def check_for_new_data():
        return _check_for_new_data()

    @task
    def make_predictions(files, source):
        return _make_predictions(files, source)

    files_to_process = check_for_new_data()
    make_predictions(files_to_process, source="scheduled")


# predict_data_dag = predict_data()
predict_data()


def _check_for_new_data():
    processed_files = Variable.get("processed_files", default_var=[], deserialize_json=True)
    all_files = os.listdir(GOOD_DATA_FOLDER)
    new_files = [f for f in all_files if f not in processed_files]
    if not new_files:
        print("No new files found in the good_data folder. Skipping prediction task.")
        raise AirflowSkipException
    Variable.set("processed_files", processed_files + new_files, serialize_json=True)
    return new_files


def _make_predictions(files, source):
    for file in files:
        file_path = os.path.join(GOOD_DATA_FOLDER, file)
        df = pd.read_csv(str(file_path))
        print(f"Processing {file_path}")
        # csv_string = df.to_csv(index=False)
        # csv_file = ("data.csv", csv_string)
        # res = requests.post(
        #     url="http://127.0.0.1:8000/predict-batch",
        #     files={"csv_file": csv_file},
        #     params={"source": source},
        # )
        # result = res.json()
        res = predict(df)
        df_res = pd.DataFrame(res, columns=["Purchase"])
        df_res = df.join(df_res)
        db_res = create_prediction_table(df_res, source=source)
        return db_res
