from pathlib import Path
import sys,os
sys.path.append(os.getcwd())
DB_HOST = "localhost"
DB_NAME = "blackfriday"
DB_USER = "ericwindsor"

DB_PORT = "5432"

# models\encoder.joblib
BASE_DIR = Path(__file__).resolve().parent.parent

# Define MODEL_PATH and ENCODER_PATH relative to BASE_DIR
MODEL_PATH = BASE_DIR / "models" / "model.joblib"
ENCODER_PATH = BASE_DIR / "models" / "encoder.joblib"

# MODEL_PATH = r'..\models\model.joblib'
# ENCODER_PATH = '..\models\encoder.joblib'
NUMERICAL_FEATURES = [
    "Occupation",
    "Marital_Status",
    "Product_Category_1",
    "Product_Category_2",
    "Product_Category_3",
]
CATEGORICAL_FEATURES = ["Age", "Gender", "City_Category", "Stay_In_Current_City_Years"]
GOOD_DATA_FOLDER = "/Users/ericwindsor/Documents/EPITA_ERIC/Data_Scicence_Production/DSP_Final/data_raw/split_data/Clean_Data"
BAD_DATA_FOLDER = "/Users/ericwindsor/Documents/EPITA_ERIC/Data_Scicence_Production/DSP_Final/data_raw/Bad_Data"
