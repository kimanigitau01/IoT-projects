from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import time
import paho.mqtt.client as mqtt
import json
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay

adc = ADC()
relay = GroveRelay(5)

id = '905726bc-8af8-422d-a2d9-2e7b19d3095d'
client_name = id + "soil-moisture-sensor"
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:",payload)

    if payload['relay_on']:
        # print("Soil Moisture is too low, turning relay on.")
        relay.on()
    else:
        # print("soil moisture is ok, turning relay off")
        relay.off()


mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command

print("MQTT connected")


while True:
    soil_moisture = adc.read(0)
    telemetry = json.dumps({'soil_moisture': soil_moisture})
    print("Sending telemetry: ", soil_moisture)

    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(10)