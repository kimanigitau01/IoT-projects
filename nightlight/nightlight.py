from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import time
import json

import paho.mqtt.client as mqtt
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed

CounterFitConnection.init('127.0.0.1', 5000)

id = 'mqtt_2sNfG9cB'
client_name = id + 'nightlight_client'
client_telemetry_topic = id + '/telemetry'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

print("MQTT connected!!")

light_sensor = GroveLightSensor(0)
led = GroveLed(5)

while True:
    light = light_sensor.light
    
    telemetry = json.dumps({'light' : light})
    print("sending telemetry ", telemetry)

    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(5)