import pandas as pd

from scripts.preprocess import preprocess
from scripts.config import MODEL_PATH
import joblib


def predict(df: pd.DataFrame) -> pd.DataFrame:
    df.drop(columns=["User_ID", "Product_ID"], inplace=True)
    df = preprocess(df)
    model = joblib.load(MODEL_PATH)
    return model.predict(df)
