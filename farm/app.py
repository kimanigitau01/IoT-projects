from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import time
from counterfit_shims_seeed_python_dht import DHT
import paho.mqtt.client as mqtt
import json

sensor = DHT("11", 5)

id = "27b87eea-e5a2-45b0-9c0f-ead981cacf16"
client_name = id + "farm_client"
client_telemetry_topic = id + "/telemetry"

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect("test.mosquitto.org")

mqtt_client.loop_start()

print("MQTT connected")

sensor = DHT("11", 5)   #(dht type, port_number)

while True:
    _, temp = sensor.read();
    telemetry = json.dumps({"temperature" : temp})
    print("sending telemetry ", telemetry)

    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(10)