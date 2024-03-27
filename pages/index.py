import streamlit as st
import requests
import ast
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

    inputs = {
        "Gender": gender,
        "Age": age,
        "Occupation": occupation,
        "City_Category": city_category,
        "Stay_In_Current_City_Years": stay_years,
        "Marital_Status": marital_status,
        "Product_Category_1": product_category_1,
        "Product_Category_2": product_category_2,
        "Product_Category_3": product_category_3,
    }

    input_vals = list(inputs.values())
    inputs = []
    inputs.append(input_vals)

    if st.button("Predict the Features"):
        res = requests.post(url="API HERE", data=json.dumps(inputs))
        json_string = res.text
        response_dict = json.loads(json_string)
        body = response_dict["Predictions"]["body"]
        body = ast.literal_eval(body)
        st.subheader(f"Predicted Quality 🚀 =  {(body[-3])}")

    file = st.file_uploader("Insert CSV FILES")

    if st.button("Make prediction"):
        csv_file = pd.read_csv(file)
        base_filename = datetime.datetime.now().strftime("%Y%m%d")
        csv_file.to_csv(f"airflow/data/Clean_Data/{base_filename}.csv", index=False)
        csv_file = csv_file.drop(["quality", "Id"], axis=1)
        features_list = csv_file.values.tolist()

        response = requests.post(url="API HERE", data=json.dumps(features_list))

        if response.status_code == 200:
            json_string = response.text
            response_dict = json.loads(json_string)
            body = response_dict["Predictions"]["body"]
            body_ = ast.literal_eval(body)
            data = json.loads(body_)
            df = pd.DataFrame(data)
            st.table(df)
        else:
            st.subheader(f"Error from API 😞 = {response.json()}")
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

    if st.button("Get Past Predictions"):
        response = requests.get(url="API HERE")

        json_string = response.text
        response_dict = json.loads(json_string)

        body = response_dict["prediction_list"]
        body = ast.literal_eval(body)

        date_list = []
        for item in body:
            created_at = item["created_at"]
            created_datetime = datetime.datetime.fromtimestamp(
                created_at / 1000
            )  # Assuming the timestamp is in milliseconds
            created_date = created_datetime.date()
            date_list.append(created_date)

        df = pd.DataFrame(body)
        df["created_date_"] = list(date_list)
        filtered_dates = [date for date in date_list if s_Date <= date <= e_Date]

        selected_columns = [
            "Gender",
            "Age",
            "City_Category",
            "Stay_In_Current_City_Years",
            "created_date_",
        ]
        df_subset = df.loc[:, selected_columns]
        filtered_df = df_subset[df_subset["created_date_"].isin(filtered_dates)]

        if response.status_code == 200:
            st.table(filtered_df)
        else:
            st.subheader(f"Error from API 😞 = {response.json()}")
