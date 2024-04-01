import pandas as pd

from scripts.save_to_db import create_prediction_table


def test_create_prediction_table():
    # Define the input dataframe
    input_data = [[1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 2.0, 3.0, 15384.5732421875]]
    columns = [
        "Occupation",
        "Marital_Status",
        "Product_Category_1",
        "Product_Category_2",
        "Product_Category_3",
        "Age",
        "Gender",
        "City_Category",
        "Stay_In_Current_City_Years",
        "Purchase",
    ]
    df = pd.DataFrame(input_data, columns=columns)

    # Call the function with the input dataframe
    result = create_prediction_table(df)
    print(result)


test_create_prediction_table()
