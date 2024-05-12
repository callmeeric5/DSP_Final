import pandas as pd

from scripts.make_ingestion_table import Ingestion_Table
from scripts.make_db import db_engine


def save_ingest_data(df: pd.DataFrame):
    try:
        session_data = db_engine()
        if session_data["status"] != 200:
            return {"status": 500, "error": "Failed to connect to database."}

        session = session_data["session"]
        ingestion_list = df.to_dict(orient="records")

        for ingest_data in ingestion_list:
            ingest = Ingestion_Table(
                occupation=ingest_data["Occupation"],
                marital_status=ingest_data["Marital_Status"],
                product_category_1=ingest_data["Product_Category_1"],
                product_category_2=ingest_data["Product_Category_2"],
                product_category_3=ingest_data["Product_Category_3"],
                age=ingest_data["Age"],
                gender=ingest_data["Gender"],
                city_category=ingest_data["City_Category"],
                stay_in_current_city_years=ingest_data["Stay_In_Current_City_Years"],
            )
            session.add(ingest)

        session.commit()
        session.close()

        print(
            {"status": 200, "message": "Ingestion data inserted/updated successfully"}
        )
    except Exception as e:
        print({"status": 500, "message": f"An error occurred: {e}"})
