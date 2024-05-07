from scripts.predict_data_dag import _check_for_new_data, _make_predictions
from datetime import datetime

files = _check_for_new_data()

predictions = _make_predictions(files, source="scheduled")
print(predictions)
