import pandas as pd
from save_prediction import create_prediction_table

# Correctly create a DataFrame from a dictionary of sample features
sample_features = {
    "User_ID": ["123"],
    "Product_ID": ["456"],
    "Gender": ["1"],
    "Age": ["17"],
    "Occupation": [1],
    "City_Category": ["1"],
    "Stay_In_Current_City_Years": ["1"],
    "Marital_Status": [0],
    "Product_Category_1": [1],
    "Product_Category_2": [2],
    "Product_Category_3": [3],
    "Purchase": [1.2],
}

# Create a DataFrame
df = pd.DataFrame(sample_features)

# Assuming create_prediction_table expects a DataFrame and a source string
result = create_prediction_table(df, source="scheduled")
print(result)
