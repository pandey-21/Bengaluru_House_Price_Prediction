import streamlit as st  
import joblib  
import numpy as np  
import json  
from babel.numbers import format_currency  

# 🎨 Custom Styling  
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f5f5;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px;
    }
    .stTextInput, .stNumberInput {
        border-radius: 8px;
    }
    h1, h3, p, label {
        color: #333333; /* Dark text for visibility */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 🚀 Load the Model  
model = joblib.load("reg1.pickle")  

# 📂 Load JSON Columns  
with open("columns.json", "r") as f:  
    data = json.load(f)  

# 📍 Extract Locations  
locations = data.get("data_columns", [])[3:]  

# 🏡 **Title & Description**  
st.markdown("<h1 style='text-align: center; color: #FF5733;'>🏡 House Price Prediction</h1>", unsafe_allow_html=True)  
st.markdown("<p style='text-align: center; font-size:18px; color: #444;'>Enter the property details below to estimate the price 💰</p>", unsafe_allow_html=True)  

# 📍 **Location Dropdown**  
feature1 = st.selectbox("📍 Select Location", locations)  

# 📊 **Feature Inputs in Two Columns for Better UI**  
col1, col2 = st.columns(2)  

with col1:  
    feature2 = st.number_input("📏 Square Feet Area", value=1000.0, min_value=100.0, step=50.0)  
    feature4 = st.number_input("🛏 Number of Bedrooms", value=2.0, min_value=1.0, step=1.0)  

with col2:  
    feature3 = st.number_input("🛁 Number of Bathrooms", value=1.0, min_value=1.0, step=1.0)  

# 📈 **Prediction Function**  
def predict_price(location, sqft, bath, bhk):    
    locations = data.get("data_columns", [])  
    x = np.zeros(len(locations))  

    # Set features  
    x[0] = sqft  
    x[1] = bath  
    x[2] = bhk  

    # Find location index  
    if location in locations:  
        loc_idx = locations.index(location)  
        x[loc_idx] = 1  

    return model.predict([x])[0]  

# 🔘 **Predict Button**  
if st.button("💰 Predict Price"):    
    prediction = predict_price(feature1, feature2, feature3, feature4)  
    full_price = prediction * 100000  # Convert from lakh to full amount  
    
    # 🏦 Format Price in Indian Style  
    formatted_price = format_currency(full_price, "INR", locale="en_IN")  

    # 🎉 **Display Prediction with Styling**  
    st.markdown(
        f"<h3 style='text-align: center; color: #228B22;'>🏡 Estimated Price: {formatted_price} </h3>",
        unsafe_allow_html=True,
    )
