import streamlit as st

page = st.sidebar.selectbox("Choose a page", ["Get Prediction", "Get Past Prediction"])

if page == "Get Prediction":
    st.title("Get Prediction")
    
    with st.form("prediction_form", clear_on_submit=True):
        gender = st.radio("Gender", ("M", "F"))
        age = st.selectbox("Age", ("0-17", "18-25", "26-35", "36-45", "46-50", "51-55", "55+"))
        occupation_options = [
            "Teacher", "Software Developer", "Nurse", "Engineer", "Doctor",
            "Salesperson", "Journalist", "Architect", "Chef", "Artist",
            "Lawyer", "Pharmacist", "Accountant", "Pilot", "Scientist",
            "Dentist", "Marketing Specialist", "Veterinarian", "Social Worker",
            "Police Officer", "Fitness Trainer"
        ]
        occupation = st.selectbox("Occupation", occupation_options)

        city_category = st.selectbox("City Category", ("Paris", "Levalois Perret", "Clichy"))
        stay_years = st.selectbox("Stay in Current City Years", ("0", "1", "2", "3", "4+"))
        marital_status = st.radio("Marital Status", ("Single", "Married"))

        cloth_categories = [
            "Hat", "T-shirt", "Jeans", "Dress", "Skirt", "Blouse", "Shorts", "Jacket",
            "Sweater", "Scarf", "Suit", "Tie", "Sportswear", "Swimwear", "Boots", "Sneakers",
            "Sandals"
        ]
        cloth_category = st.selectbox("Cloth Category", cloth_categories) 

        electronic_options = ["None"] + [
            "Smartphone", "Laptop", "Tablet", "Smartwatch", "E-reader", "Portable Speaker",
            "Headphones", "Digital Camera", "Gaming Console", "VR Headset", "Fitness Tracker",
            "Drone", "Keyboard", "Mouse", "External Hard Drive", "USB Flash Drive", "Power Bank"
        ]
        electronic = st.selectbox("Electronic", electronic_options, index=0)

        home_good_options = ["None"] + [
        "Blender", "Microwave", "Toaster", "Coffee Maker", "Vacuum Cleaner", "Rice Cooker",
        "Electric Kettle", "Slow Cooker", "Air Purifier", "Iron", "Sewing Machine",
        "Humidifier", "Dishwasher", "Refrigerator", "Washing Machine", "Dryer"
        ]
        home_good = st.selectbox("Home Good", home_good_options, index=0)

        submitted = st.form_submit_button("Submit")
        """
        Index(['User_ID', 'Product_ID', 'Gender', 'Age', 'Occupation', 'City_Category',
       'Stay_In_Current_City_Years', 'Marital_Status', 'Product_Category_1',
       'Product_Category_2', 'Product_Category_3', 'Purchase'],
        dtype='object')
        """
    if submitted:
            user_data = {
                "User_ID": "U0111",
                "Product_ID": "P09183",
                "Gender": gender,
                "Age": age,
                "Occupation": occupation_options.index(occupation),
                "city_category": city_category,
                "Stay_In_Current_City_Years": stay_years,
                "Marital_Status": 0 if marital_status == "Single" else 1,
                "Product_Category_1": cloth_categories.index(cloth_category) + 1,
                "Product_Category_2": None if electronic == "None" else electronic_options.index(electronic),
                "Product_Category_3": None if home_good == "None" else home_good_options.index(home_good)+1
            }
            if user_data["Product_Category_2"] is not None:
                user_data["Product_Category_2"] += 1  
            if user_data["Product_Category_3"] is not None:
                user_data["Product_Category_3"] += 2

            st.success("Form submitted!")
            #Make it json for API
            st.json(user_data)

elif page == "Get Past Prediction":
    st.title("Get Past Prediction")
    
    with st.form("past_prediction_form", clear_on_submit=True):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            st.success("Form submitted! We'll send your past predictions to your email.")

