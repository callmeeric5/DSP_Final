import pandas as pd

from scripts.make_predticiton_table import Prediction_Table
from scripts.make_db import db_engine


def create_prediction_table(predictions_df: pd.DataFrame, source: str = "webapp"):
    try:
        session_data = db_engine()
        if session_data["status"] == 200:
            session = session_data["session"]

            predictions_list = predictions_df.to_dict(orient="records")

            for prediction_data in predictions_list:
                prediction = Prediction_Table(
                    occupation=prediction_data["Occupation"],
                    marital_status=prediction_data["Marital_Status"],
                    product_category_1=prediction_data["Product_Category_1"],
                    product_category_2=prediction_data["Product_Category_2"],
                    product_category_3=prediction_data["Product_Category_3"],
                    age=prediction_data["Age"],
                    gender=prediction_data["Gender"],
                    city_category=prediction_data["City_Category"],
                    stay_in_current_city_years=prediction_data[
                        "Stay_In_Current_City_Years"
                    ],
                    purchase=prediction_data["Purchase"],
                    source=source,
                )
                session.add(prediction)

            session.commit()
            session.close()

            return {
                "status": 200,
                "message": "Prediction data inserted/updated successfully",
                "source": source,
            }
        else:
            return {"status": 500, "message": "Failed to obtain database session."}
    except Exception as e:
        return {"status": 500, "message": f"An error occurred: {e}"}
