from .make_db import db_engine
import pandas as pd

from .make_predticiton_table import Prediction_Table


def create_prediction_table(predictions: pd.DataFrame, source: str = "webapp"):
    try:
        session_data = db_engine()

        if session_data["status"] == 200:
            session = session_data["session"]

            with session.begin():
                for index, row in predictions.iterrows():
                    prediction = Prediction_Table(
                        occupation=row["Occupation"],
                        marital_status=row["Marital_Status"],
                        product_category_1=row["Product_Category_1"],
                        product_category_2=row["Product_Category_2"],
                        product_category_3=row["Product_Category_3"],
                        age=row["Age"],
                        gender=row["Gender"],
                        city_category=row["City_Category"],
                        stay_in_current_city_years=row["Stay_In_Current_City_Years"],
                        predicted_purchase=row["Predicted_Purchase"],
                        source=source,
                    )
                    session.add(prediction)
            return {"status": 200, "message": "Prediction data inserted successfully"}
        else:
            return {"status": 500, "message": "Failed to obtain database session."}
    except Exception as e:
        return {"status": 500, "message": f"An error occurred: {e}"}
