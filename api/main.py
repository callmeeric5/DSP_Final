from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
from fastapi import Depends
from sqlalchemy.orm import Session
import pandas as pd
from scripts.save_to_db import create_prediction_table
from scripts.inference import predict
from scripts.get_past_prediction import get_past_predictions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from fastapi.responses import JSONResponse
from datetime import datetime
from fastapi import Query

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


@app.post("/predict_single")
def predict_single(features: Features, source: str = "webapp"):
    try:
        features_dict = features.model_dump()
        correct_order_columns = [
            "User_ID",
            "Product_ID",
            "Gender",
            "Age",
            "Occupation",
            "City_Category",
            "Stay_In_Current_City_Years",
            "Marital_Status",
            "Product_Category_1",
            "Product_Category_2",
            "Product_Category_3",
        ]

        features_list = [features_dict[col] for col in correct_order_columns]

        df = pd.DataFrame([features_list], columns=correct_order_columns)

        res = predict(df)

        df_res = pd.DataFrame(res, columns=["Purchase"])

        df_with_pred = pd.concat([df, df_res], axis=1)

        db_res = create_prediction_table(df_with_pred, source=source)

        return JSONResponse(
            status_code=200,
            content={
                "status": 200,
                "message": "Successful",
                "results": df_with_pred.values.tolist(),
                "db_res": db_res,
            },
        )
    except Exception as e:
        logging.error(f"An error occurred in predict_single: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/predict-batch")
def predict_batch(csv_file: UploadFile, source: str = "webapp"):
    try:
        df = pd.read_csv(csv_file.file)
        res = predict(df)
        df_res = pd.DataFrame(res, columns=["Purchase"])
        df_res = df.join(df_res)
        db_res = create_prediction_table(df_res, source=source)
        return {
            "status": 200,
            "message": "Successful-1111",
            "results": df_res.values.tolist(),
            "db_res": db_res,
        }
    except Exception as e:
        logging.error(f"An error occurred in predict_batch: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/past-predictions")
def get_predictions(filter_option: str, start_date: str, end_date: str):
    try:
        # parsed_start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        # parsed_end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
        predictions_data = get_past_predictions(filter_option, start_date, end_date)
        return predictions_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
