import streamlit as st
import requests
import ast
import datetime
import json
import pandas as pd

st.set_page_config(page_title="Black Friday", page_icon="shopping_cart", layout="wide")


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


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
                     - User_ID\n
                     - Product_ID\n
                     - Gender\n
                     - Age\n
                     - Occupation\n
                     - City_Category\n
                     - Stay_In_Current_City_Years\n
                     - Marital_Status\n
                     - Product_Category_1\n
                     - Product_Category_2\n
                     - Product_Category_3\n
                     - Purchase"""
        )

    with right_column:
        User_ID = st.number_input("User_ID", format="%.5f")
        Product_ID = st.number_input("Product_ID", format="%.5f")
        Gender = st.number_input("Gender", format="%.5f")
        Age = st.number_input("Age", format="%.5f")
        Occupation = st.number_input("Occupation", format="%.5f")
        City_Category = st.number_input("City_Category", format="%.5f")
        Stay_In_Current_City_Years = st.number_input("Stay_In_Current_City_Years", format="%.5f")
        Marital_Status = st.number_input("Marital_Status", format="%.5f")
        Product_Category_1 = st.number_input("Product_Category_1", format="%.5f")
        Product_Category_2 = st.number_input("Product_Category_2", format="%.5f")
        Product_Category_3 = st.number_input("Product_Category_3", format="%.5f")
        Purchase = st.number_input("Purchase", format="%.5f")

inputs = {
    "User_ID": User_ID,
    "Product_ID": Product_ID,
    "Gender": Gender,
    "Age": Age,
    "Occupation": Occupation,
    "City_Category": City_Category,
    "Stay_In_Current_City_Years": Stay_In_Current_City_Years,
    "Marital_Status": Marital_Status,
    "Product_Category_1": Product_Category_1,
    "Product_Category_2": Product_Category_2,
    "Product_Category_3": Product_Category_3,
    'Purchase': Purchase
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

    response = requests.post(
        url="API HERE", data=json.dumps(features_list)
    )

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
