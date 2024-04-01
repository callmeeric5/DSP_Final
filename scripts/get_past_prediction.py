import pandas as pd
from .make_predticiton_table import Prediction_Table
from .make_db import db_engine


def get_past_predictions(filter_option):
    try:
        session_data = db_engine()
        if session_data["status"] == 200:
            session = session_data["session"]
            past_predictions = []
            if filter_option == "webapp":
                result = (
                    session.query(Prediction_Table)
                    .filter(Prediction_Table.source == "webapp")
                    .all()
                )
            elif filter_option == "scheduled":
                result = (
                    session.query(Prediction_Table)
                    .filter(Prediction_Table.source == "scheduled")
                    .all()
                )
            elif filter_option == "all":
                result = session.query(Prediction_Table).all()
            else:
                raise ValueError(
                    "Invalid filter option. Use 'webapp', 'scheduled', or 'all'."
                )

            for item in result:
                prediction_dict = {
                    "id": item.id,
                    "occupation": item.occupation,
                    "marital_status": item.marital_status,
                    "product_category_1": item.product_category_1,
                    "product_category_2": item.product_category_2,
                    "product_category_3": item.product_category_3,
                    "age": item.age,
                    "gender": item.gender,
                    "city_category": item.city_category,
                    "stay_in_current_city_years": item.stay_in_current_city_years,
                    "predicted_purchase": item.predicted_purchase,
                    "source": item.source,
                    "created_at": item.created_at,
                }
                past_predictions.append(prediction_dict)
            df = pd.DataFrame(past_predictions)
            return {"data": df.to_json(orient="records"), "status": 200}
        else:
            return {"data": {}, "status": 500}
    except Exception as e:
        print(e.args)
        return {"data": {}, "status": 500}
