import time
import json
import random
import paho.mqtt.client as mqtt

BROKER = "mqtt.eclipseprojects.io"
PORT = 1883
TOPIC = "data"


def generate_synthetic_crop_data():
    return {
        "Nitrogen": random.randint(0, 140),
        "Phosphorous": random.randint(5, 145),
        "Potassium": random.randint(5, 205),
        "temperature": round(random.uniform(8.8, 43.7), 2),
        "humidity": round(random.uniform(14.25, 99.98), 2),
        "ph": round(random.uniform(3.5, 9.93), 2),
        "rainfall": round(random.uniform(20.21, 298.56), 2),
    }


def publish_loop():
    client = mqtt.Client()
    client.connect(BROKER, PORT)
    client.loop_start()

    try:
        while True:
            payload = generate_synthetic_crop_data()
            client.publish(TOPIC, json.dumps(payload))
            print(f" sensor input generated → {TOPIC}: {payload}")
            time.sleep(5)

    except KeyboardInterrupt:
        print(" Publishing stopped by user.")

    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    publish_loop()
