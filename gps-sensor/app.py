from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import time
import json
import pynmea2
import counterfit_shims_serial
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

connection_string = "HostName=gps-sensor.azure-devices.net;DeviceId=gps-sensor;SharedAccessKey=YpUGkcc8MhLMvX59DmMebwR+KlKJ/JPk33O67fP8q8c="

device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

print('Connecting')
device_client.connect()
print('Connected')
serial = counterfit_shims_serial.Serial('/dev/ttyAMA0')

def print_gps_data(line):
    msg = pynmea2.parse(line)

    if msg.sentence_type == 'GGA':
        lat = pynmea2.dm_to_sd(msg.lat)
        lon = pynmea2.dm_to_sd(msg.lon)

        if msg.lat_dir == 'S':
            lat = lat * -1

        if msg.lon_dir == 'W':
            lon = lon * -1

        message_json = { "gps" : { "lat":lat, "lon":lon } }
        print("Sending telemetry", message_json)
        message = Message(json.dumps(message_json))
        device_client.send_message(message)


while True:
    line = serial.readline().decode('utf-8')

    while len(line) > 0:
        print_gps_data(line)
        line = serial.readline().decode('utf-8')

    time.sleep(1)