# # from scripts.make_db import db_engine
# # from sqlalchemy import text
# #
# # # Obtain the session
# # session_data = db_engine()
# # session = session_data["Session"]()
# #
# # # Define the SQL query
# # sql_query = 'SELECT * FROM "Prediction_Table" WHERE source = \'webapp\';'
# #
# #
# # # Execute the query
# # result = session.execute(text(sql_query))
# #
# # # Fetch the results
# # rows = result.fetchall()
# #
# # # Process the results as needed
# # for row in rows:
# #     # Do something with each row
# #     print(row)
#
# from scripts.make_predticiton_table import Prediction_Table
# from scripts.make_db import db_engine
# from sqlalchemy.orm import sessionmaker
# #
# session_data = db_engine()
# past_predictions = []
# Session = session_data["Session"]
# session = Session()
# query = session.query(Prediction_Table)
#
# query = query.filter(Prediction_Table.source == "webapp")
# query = query.filter(Prediction_Table.created_at >= '2024-04-02')
#
# query = query.filter(Prediction_Table.created_at <= '2024-04-03')
# result = query.all()
# for item in result:
#                 prediction_dict = {
#                     "id": item.id,
#                     "occupation": item.occupation,
#                     "marital_status": item.marital_status,
#                     "product_category_1": item.product_category_1,
#                     "product_category_2": item.product_category_2,
#                     "product_category_3": item.product_category_3,
#                     "age": item.age,
#                     "gender": item.gender,
#                     "city_category": item.city_category,
#                     "stay_in_current_city_years": item.stay_in_current_city_years,
#                     "purchase": item.purchase,
#                     "source": item.source,
#                     "created_at": item.created_at,
#                 }
#                 past_predictions.append(prediction_dict)
#
# session.close()
# print(past_predictions)
import requests


# def test_get_predictions():
#     # Define a list of filter options to test
#     filter_options = ["webapp", "scheduled", "all"]
#
#     # Iterate over each filter option
#     for filter_option in filter_options:
#         # Make a GET request to the API endpoint with the current filter option
#         response = requests.get(f"http://localhost:8000/past-predictions?filter_option={filter_option}")
#
#         # Check if the request was successful (status code 200)
#         if response.status_code == 200:
#             # Print the response data
#             print(f"Filter Option: {filter_option}")
#             print("Response:")
#             print(response.json())
#         else:
#             print(f"Failed to get predictions for filter option {filter_option}. Error:", response.status_code)
# import requests
#
# url = "http://localhost:8000/past-predictions"
# params = {
#     "filter_option": "webapp",
#     "start_date": "2024-04-02",
#     "end_date": "2024-04-03",
# }
#
# response = requests.get(url, params=params)
#
# print(response.json())

# Run the test
# test_get_predictions()

# from scripts.get_past_prediction import get_past_predictions
# res = get_past_predictions('webapp','2024-04-02','2024-04-03')
# print(res)
from scripts.split_data import split_dataset

split_dataset()
