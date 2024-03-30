import streamlit as st
import requests

import datetime
import json
import pandas as pd

st.set_page_config(page_title="Black Friday", page_icon="🛍️", layout="wide")
page = st.sidebar.selectbox("Choose a page", ["Get Prediction", "Get Past Prediction"])

if page == "Get Prediction":
    with st.container():
        st.title("Black Friday Prediction")
        st.header("DSP - EPITA")

    with st.container():
        st.write("-----")
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("Description")
            st.write("##")
            st.write(
                """Hello World?Hello WorldHello WorldHello WorldHello WorldHello 
                WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello 
                WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello 
                WorldHello WorldHello WorldHello WorldHello WorldHello 
                WorldHello WorldHello WorldHello WorldHello WorldHello 
                WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello 
                WorldHello WorldHello World"""
            )
            st.write(
                "[Learn More >](https://www.kaggle.com/datasets/sdolezel/black-friday/code)"
            )

            st.header("Features used to Predict")
            st.write("##")
            st.write(
                """Input variables:\n
                         Features:\n
                         - Gender\n
                         - Age\n
                         - Occupation\n
                         - City_Category\n
                         - Stay_In_Current_City_Years\n
                         - Marital_Status\n
                         - Product_Category_1\n
                         - Product_Category_2\n
                         - Product_Category_3
                         """
            )

        with right_column:
            gender = st.radio("Gender", ("M", "F"))
            age = st.selectbox(
                "Age", ("0-17", "18-25", "26-35", "36-45", "46-50", "51-55", "55+")
            )
            occupation_options = [
                "Teacher",
                "Software Developer",
                "Nurse",
                "Engineer",
                "Doctor",
                "Salesperson",
                "Journalist",
                "Architect",
                "Chef",
                "Artist",
                "Lawyer",
                "Pharmacist",
                "Accountant",
                "Pilot",
                "Scientist",
                "Dentist",
                "Marketing Specialist",
                "Veterinarian",
                "Social Worker",
                "Police Officer",
                "Fitness Trainer",
            ]
            occupation = st.selectbox("Occupation", occupation_options)
            city_category = st.selectbox(
                "City Category", ("Paris", "Levalois Perret", "Clichy")
            )
            stay_years = st.selectbox(
                "Stay in Current City Years", ("0", "1", "2", "3", "4+")
            )
            marital_status = st.radio("Marital Status", ("Single", "Married"))
            cloth_categories = [
                "Hat",
                "T-shirt",
                "Jeans",
                "Dress",
                "Skirt",
                "Blouse",
                "Shorts",
                "Jacket",
                "Sweater",
                "Scarf",
                "Suit",
                "Tie",
                "Sportswear",
                "Swimwear",
                "Boots",
                "Sneakers",
                "Sandals",
            ]
            product_category_1 = st.selectbox("Cloth Categories", cloth_categories)
            electronic_options = ["None"] + [
                "Smartphone",
                "Laptop",
                "Tablet",
                "Smartwatch",
                "E-reader",
                "Portable Speaker",
                "Headphones",
                "Digital Camera",
                "Gaming Console",
                "VR Headset",
                "Fitness Tracker",
                "Drone",
                "Keyboard",
                "Mouse",
                "External Hard Drive",
                "USB Flash Drive",
                "Power Bank",
            ]
            product_category_2 = st.selectbox(
                "Electronic Options", electronic_options, index=0
            )
            home_good_options = ["None"] + [
                "Blender",
                "Microwave",
                "Toaster",
                "Coffee Maker",
                "Vacuum Cleaner",
                "Rice Cooker",
                "Electric Kettle",
                "Slow Cooker",
                "Air Purifier",
                "Iron",
                "Sewing Machine",
                "Humidifier",
                "Dishwasher",
                "Refrigerator",
                "Washing Machine",
                "Dryer",
            ]
            product_category_3 = st.selectbox(
                "Home Good Options", home_good_options, index=0
            )
    city_category_mapping = {
        "Paris": "A",
        "Levalois Perret": "B",
        "Clichy": "C",
    }
    city_category_letter = city_category_mapping.get(city_category, "Unknown")
    inputs = {
        "User_ID": "Notneeded",
        "Product_ID": "Notneeded",
        "Gender": gender,
        "Age": age,
        "Occupation": occupation_options.index(occupation),
        "City_Category": city_category_letter,
        "Stay_In_Current_City_Years": stay_years,
        "Marital_Status": 0 if marital_status == "Single" else 1,
        "Product_Category_1": cloth_categories.index(product_category_1) + 1,
        "Product_Category_2": None if product_category_2 == "None" else electronic_options.index(product_category_2),
        "Product_Category_3": None if product_category_3 == "None" else home_good_options.index(product_category_3) + 1
        # "Product_Category_2": product_category_2 if product_category_2 != "None" else "",
        # "Product_Category_3": product_category_3 if product_category_3 != "None" else "",
    }
    if inputs["Product_Category_2"] is not None:
        inputs["Product_Category_2"] += 1
    if inputs["Product_Category_3"] is not None:
       inputs["Product_Category_3"] += 2


    # input_vals = list(inputs.values())
    # inputs = []
    # inputs.append(input_vals)
    if st.button("Predict the Features"):
        res = requests.post(
            url="http://127.0.0.1:8000/predict_single", 
            #data=json.dumps(inputs)
            json=inputs
        )
        if res.status_code == 200:
            result = res.json()
            st.success("Prediction successful.")
            st.write(result)
        else:
            st.error(f"Failed to get prediction. Please try again later. Error: {res.status_code}")
            error_details = res.json()
            st.write("Error Details:", error_details)  

    file = st.file_uploader("Insert CSV FILES")

    if st.button("Make prediction"):
        if file is None:
            st.error("Please upload a CSV file.")
        else:
            csv_file = pd.read_csv(file)
            base_filename = datetime.datetime.now().strftime("%Y%m%d")
            csv_file.to_csv(f"airflow/data/Clean_Data/{base_filename}.csv", index=False)
            csv_file = csv_file.drop(["quality", "Id"], axis=1)
            features_list = csv_file.values.tolist()

            response = requests.post(
                url="http://127.0.0.1:8000/predict-batch",
                data=json.dumps(features_list),
            )
            if response.status_code == 200:
                predictions_df = pd.read_json(response.json()["data"], orient="records")
                st.dataframe(predictions_df)
            else:
                st.error("Failed to make prediction. Please try again later.")

elif page == "Get Past Prediction":
    with st.container():
        st.title("Black Friday Prediction History")
        st.header("DSP - EPITA")

    with st.container():
        st.write("-----")
        left_column, right_column = st.columns(2)
        with left_column:
            s_Date = st.date_input("Start Date")
        with right_column:
            e_Date = st.date_input("End Date")

        filter_option = st.selectbox(
            "Prediction source", ["webapp", "scheduled", "all"]
        )

    if st.button("Get Past Predictions"):
        response = requests.get(
            url="http://127.0.0.1:8000/past-predictions",
            params={"filter": filter_option},
        )

        if response.status_code == 200:
            past_predictions_df = pd.read_json(
                response.json()["data"], orient="records"
            )
            st.dataframe(past_predictions_df)
        else:
            st.error("Failed to get past predictions. Please try again later.")
