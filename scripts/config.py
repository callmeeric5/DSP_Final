DB_HOST = "localhost"
DB_NAME = "Blackfriday"
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_PORT = "0224"

MODEL_PATH = "../models/model.joblib"
ENCODER_PATH = "../models/encoder.joblib"
NUMERICAL_FEATURES = [
    "Occupation",
    "Marital_Status",
    "Product_Category_1",
    "Product_Category_2",
    "Product_Category_3",
]
CATEGORICAL_FEATURES = ["Age", "Gender", "City_Category", "Stay_In_Current_City_Years"]
