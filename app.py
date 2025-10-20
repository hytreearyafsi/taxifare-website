import streamlit as st
import requests
from datetime import datetime

# ---- Title ----
st.title("🚕 Taxi Fare Prediction App")

st.markdown("""
This app estimates the taxi fare in New York City using Le Wagon’s prediction API.
Please enter the ride details below 👇
""")

# ---- 1. Collect user inputs ----
pickup_date = st.date_input("Pickup date")
pickup_time = st.time_input("Pickup time", value=datetime.now().time())

pickup_longitude = st.number_input("Pickup longitude", value=-73.985428)
pickup_latitude = st.number_input("Pickup latitude", value=40.748817)
dropoff_longitude = st.number_input("Dropoff longitude", value=-73.985428)
dropoff_latitude = st.number_input("Dropoff latitude", value=40.748817)
passenger_count = st.number_input("Passenger count", min_value=1, max_value=8, value=1)

# Combine date and time
pickup_datetime = datetime.combine(pickup_date, pickup_time)

# ---- 2. API URL ----
url = "https://taxifare.lewagon.ai/predict"

# ---- 3. Create parameters dictionary ----
params = {
    "pickup_datetime": pickup_datetime.strftime("%Y-%m-%d %H:%M:%S"),
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": int(passenger_count)
}

# ---- 4. Call the API ----
if st.button("Predict fare"):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        prediction = response.json()
        st.success(f"💰 Estimated fare: **${prediction['fare']:,.2f}**")
    else:
        st.error(f"❌ Error {response.status_code}: {response.text}")
