from make_train_table import Train_Table
from make_db import db_engine
import pandas as pd


def save_train_data(df: pd.DataFrame):
    try:
        session_data = db_engine()
        if session_data["status"] != 200:
            return {"status": 500, "error": "Failed to connect to database."}

        session = session_data["session"]
        train_list = df.to_dict(orient="records")

        for train_data in train_list:
            train = Train_Table(
                occupation=train_data["Occupation"],
                marital_status=train_data["Marital_Status"],
                product_category_1=train_data["Product_Category_1"],
                product_category_2=train_data["Product_Category_2"],
                product_category_3=train_data["Product_Category_3"],
                age=train_data["Age"],
                gender=train_data["Gender"],
                city_category=train_data["City_Category"],
                stay_in_current_city_years=train_data["Stay_In_Current_City_Years"],
            )
            session.add(train)

        session.commit()
        session.close()

        return {
            "status": 200,
            "message": "Train data inserted/updated successfully",
        }
    except Exception as e:
        return {"status": 500, "message": f"An error occurred: {e}"}
