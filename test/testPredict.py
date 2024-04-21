from scripts.predict_data_dag import _check_for_new_data,_make_predictions
import os
from scripts.__init__ import GOOD_DATA_FOLDER
files = _check_for_new_data()

predictions = _make_predictions(files, source="scheduled")
print(predictions)


