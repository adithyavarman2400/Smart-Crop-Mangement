import streamlit as st
import json
import time
import os

st.set_page_config(page_title="Crop Predictor", layout="centered")
st.title("Smart Crop Prediction")

sensor_placeholder = st.empty()
prediction_placeholder = st.empty()

st.markdown("Sensor Data Incomming")

while True:
    if os.path.exists("latest_prediction.json"):
        with open("latest_prediction.json", "r") as f:
            try:
                data = json.load(f)
                sensor = data.get("sensor_data", {})
                pred = data.get("prediction", "N/A")

                sensor_placeholder.markdown(f"Sensor Data\n```json\n{json.dumps(sensor, indent=2)}\n```")
                prediction_placeholder.success(f"Ideal For:** `{pred}`")

            except json.JSONDecodeError:
                st.warning("Invalid JSON format. Waiting for update...")

    time.sleep(1)
