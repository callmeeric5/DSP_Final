import pandas as pd

from scripts.save_to_db import create_prediction_table
from scripts.save_log import save_data_logs


def test_create_prediction_table():
    # Define the input dataframe
    error_dict = {
        "meta": {"run_id": "12345", "other_meta_info": "info"},
        "errors": [{"column": "name", "error": "invalid data"}],
    }
    save_data_logs(error_dict)


test_create_prediction_table()
