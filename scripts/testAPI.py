import requests


def test_predict_single():
    # Define sample features data
    sample_features = {
        "User_ID": "123",
        "Product_ID": "456",
        "Gender": "M",
        "Age": "0-17",
        "Occupation": 1,
        "City_Category": "A",
        "Stay_In_Current_City_Years": "1",
        "Marital_Status": 0,
        "Product_Category_1": 1,
        "Product_Category_2": 2,
        "Product_Category_3": 3,
    }

    # Make a POST request to the predict_single endpoint with sample features data
    response = requests.post(
        url="http://127.0.0.1:8000/predict_single", json=sample_features
    )

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("Prediction request successful.")
        # Print the response data
        print("Response:")
        print(response.json())
    else:
        print("Failed to get prediction. Error:", response.status_code)


# Run the test
test_predict_single()
