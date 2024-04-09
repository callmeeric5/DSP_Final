from scripts.make_db import db_engine

from scripts.make_predticiton_table import Prediction_Table


def get_past_predictions(
    filter_option: str, start_date: str = None, end_date: str = None
):
    try:
        session_data = db_engine()
        print(session_data)
        if session_data["status"] == 200:
            session = session_data["session"]  # Access session object correctly
            past_predictions = []

            # Construct the base query
            query = session.query(Prediction_Table)

            # Apply filter_option
            if filter_option == "webapp":
                query = query.filter(Prediction_Table.source == "webapp")
            elif filter_option == "scheduled":
                query = query.filter(Prediction_Table.source == "scheduled")
            elif filter_option == "all":
                query = query.filter(Prediction_Table.source == "all")

            # Apply date filters
            if start_date:
                query = query.filter(Prediction_Table.created_at >= start_date)
            if end_date:
                query = query.filter(Prediction_Table.created_at <= end_date)

            # Execute the query
            result = query.all()

            # Convert the results to dictionary format
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
                    "purchase": item.purchase,
                    "source": item.source,
                    "created_at": item.created_at,
                }
                past_predictions.append(prediction_dict)
            session.close()

            return past_predictions
        else:
            return {"data": {}, "status": 500}
    except Exception as e:
        return {"data": {e}, "status": 500}
