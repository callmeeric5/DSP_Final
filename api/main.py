from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
from fastapi import Depends
from typing import List
from sqlalchemy.orm import Session
import pandas as pd
from scripts.save_to_db import create_prediction_table
from scripts.inference import predict
from scripts.get_past_prediction import get_past_predictions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

app = FastAPI()

# DATABASE_URL = "postgresql://admin:admin@localhost:0224/Blackfriday"
# engine = create_engine(DATABASE_URL)
# Session = sessionmaker(bind=engine)

DATABASE_URL = "postgresql://admin:admin@localhost:0224/Blackfriday"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logging.basicConfig(level=logging.ERROR)


class Features(BaseModel):
    User_ID: str
    Product_ID: str
    Occupation: int
    Marital_Status: int
    Product_Category_1: int
    Product_Category_2: int
    Product_Category_3: int
    Age: str
    Gender: str
    City_Category: str
    Stay_In_Current_City_Years: str


@app.get("/")
async def read_root():
    return {"message": "Hello, World"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/predict_single")
def predict_single(features: Features, source: str = "webapp"):
    try:
        features_dict = features.dict()
        #df = pd.DataFrame.from_dict([features_dict])
        correct_order_columns = ['User_ID', 'Product_ID',
            'Gender', 'Age', 'Occupation', 'City_Category', 
            'Stay_In_Current_City_Years', 'Marital_Status', 
            'Product_Category_1', 'Product_Category_2', 'Product_Category_3'
        ]
        df = pd.DataFrame([features_dict], columns=correct_order_columns)
        res = predict(df)
        df_res = pd.DataFrame(res, columns=["Purchase"])
        df_res = df.join(df_res)
        create_prediction_table(df_res, source=source)
        return {
            "status": 200,
            "message": "Successful",
            "results": df_res.values.tolist(),
        }
    except Exception as e:
        logging.error(f"An error occurred in predict_single: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/predict-batch")
def predict_batch(csv_file: UploadFile):
    try:
        df = pd.read_csv(csv_file.file)
        res = predict(df)
        df_res = pd.DataFrame(res, columns=["Purchase"])
        df_res = df.join(df_res)
        create_prediction_table(df_res)
        return {
            "status": 200,
            "message": "Successful-1111",
            "results": df_res.values.tolist(),
        }
    except Exception as e:
        logging.error(f"An error occurred in predict_batch: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_predictions(filter_option: str, db: Session = Depends(get_db)):
    try:
        predictions_data = get_past_predictions(filter_option)
        return predictions_data
    except Exception as e:
        logging.error(f"An error occurred in get_predictions: {e}")
        raise HTTPException(status_code=500, detail=str(e))
