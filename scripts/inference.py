import pandas as pd

from scripts.preprocess import preprocess
from scripts.__init__ import MODEL_PATH
import joblib
from scripts.save_ingestion import save_ingest_data


def predict(df: pd.DataFrame) -> pd.DataFrame:
    df.drop(columns=["User_ID", "Product_ID"], inplace=True)
    df = preprocess(df)
    save_ingest_data(df)
    model = joblib.load(MODEL_PATH)
    return model.predict(df)
