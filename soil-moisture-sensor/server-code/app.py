import json 
import time

import threading
import paho.mqtt.client as mqtt

id = '905726bc-8af8-422d-a2d9-2e7b19d3095d'
client_name = id + "soil-moisture-sensor-server"
client_telemetry_topic = id + '/telemetry'

server_command_topic = id + '/commands'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

water_time = 5
wait_time = 20
def send_relay_command(client,state):
    command = {'relay_on' : state}
    print("Sending message:", command)
    client.publish(server_command_topic, json.dumps(command))

def control_relay(client):
    print("Unsubscribing from telemetry")
    mqtt_client.unsubscribe(client_telemetry_topic)

    send_relay_command(client, True)
    time.sleep(water_time)
    send_relay_command(client, False)

    time.sleep(wait_time)

    print("Subscribing to telemetry")
    mqtt_client.subscribe(client_telemetry_topic)

def handle_telemetry(client, userdata, message):
    payload =json.loads(message.payload.decode())
    print("Message received: ", payload)

    if payload['soil_moisture'] >450:
        threading.Thread(target =control_relay, args = (client,)).start()
        
    command = {'relay_on': payload['soil_moisture'] > 450}
    print("Sending message: ", command)
    client.publish(server_command_topic, json.dumps(command))

mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(2)