import paho.mqtt.client as mqtt
import json
import pickle
import pandas as pd

broker = "mqtt.eclipseprojects.io"
port = 1883
topic = "data"

with open("random_forest.pkl", "rb") as f:
    model = pickle.load(f)

feature_keys = ['Nitrogen', 'Phosphorous', 'Potassium', 'temperature', 'humidity', 'ph', 'rainfall']


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(topic)
    else:
        print(f"Connection failed with code {rc}")


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print(f"Received: {data}")

        if all(key in data for key in feature_keys):
            df = pd.DataFrame([data], columns=feature_keys)
            prediction = model.predict(df)[0]
            output = {
                "sensor_data": data,
                "prediction": prediction
            }
            with open("latest_prediction.json", "w") as f:
                json.dump(output, f)
        else:
            print("Missing fields, skipping.")

    except Exception as e:
        print("Error:", e)


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(broker, port, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nDisconnected from MQTT broker by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
