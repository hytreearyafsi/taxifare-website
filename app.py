import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# ---- Title ----
st.title("🚕 Taxi Fare Prediction App 🎉")
st.markdown("This app estimates the taxi fare in NYC using Le Wagon’s prediction API. Enter ride details below 👇")

# ---- Inputs ----
pickup_date = st.date_input("Pickup date")
pickup_time = st.time_input("Pickup time", value=datetime.now().time())

pickup_longitude = st.number_input("Pickup longitude", value=-73.985428)
pickup_latitude = st.number_input("Pickup latitude", value=40.748817)
dropoff_longitude = st.number_input("Dropoff longitude", value=-73.985428)
dropoff_latitude = st.number_input("Dropoff latitude", value=40.748817)
passenger_count = st.number_input("Passenger count", min_value=1, max_value=8, value=1)

pickup_datetime = datetime.combine(pickup_date, pickup_time)

# ---- API call setup ----
url = "https://taxifare.lewagon.ai/predict"
params = {
    "pickup_datetime": pickup_datetime.strftime("%Y-%m-%d %H:%M:%S"),
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": int(passenger_count)
}

# ---- Map ----
st.header("🗺 Ride Map")
df_map = pd.DataFrame({
    'lat': [pickup_latitude, dropoff_latitude],
    'lon': [pickup_longitude, dropoff_longitude],
})
st.map(df_map)

# ---- Fare Prediction ----
st.header("💰 Fare Prediction")
if st.button("Predict fare"):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        prediction = response.json()
        st.success(f"💵 Estimated fare: **${prediction['fare']:,.2f}**")

        # ---- Flying cats ----
        flying_cats = """
        <div style="position: relative; width: 100%; height: 400px; overflow: hidden;">
        <style>
        .cat {
            position: absolute;
            font-size: 2rem;
            user-select: none;
            pointer-events: none;
            animation-name: float;
            animation-iteration-count: infinite;
            animation-timing-function: linear;
        }
        @keyframes float {
            0% { transform: translateY(400px) rotate(0deg); }
            50% { transform: translateY(200px) rotate(180deg); }
            100% { transform: translateY(-50px) rotate(360deg); }
        }
        </style>
        <script>
        const catEmojis = ['🐱','😸','😹','😺','😻','😼'];
        for(let i=0; i<20; i++){
            const cat = document.createElement('div');
            cat.className = 'cat';
            cat.style.left = Math.random()*90 + 'vw';
            cat.style.top = Math.random()*90 + 'px';
            cat.style.animationDuration = (3 + Math.random()*5) + 's';
            cat.innerHTML = catEmojis[Math.floor(Math.random()*catEmojis.length)];
            document.currentScript.parentNode.appendChild(cat);
        }
        </script>
        </div>
        """
        st.components.v1.html(flying_cats, height=400)

    else:
        st.error(f"❌ Error {response.status_code}: {response.text}")

# ---- NYC fact ----
st.markdown("✨ **Did you know?** The average NYC taxi ride is about 2.3 miles!")
