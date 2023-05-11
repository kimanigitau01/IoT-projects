from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import time 
import json
import counterfit_shims_serial
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

serial = counterfit_shims_serial.Serial('/dev/ttyAMA0')
connection_string = "HostName=gps-sensor-1.azure-devices.net;DeviceId=gps-sensor;SharedAccessKey=VqetOmzZD4u/UO2dI0MVGEyVK7JCwuzzdbhV5rSNpuc="

device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

print('connecting')
device_client.connect()
print('Connected')

import pynmea2

def print_gps_data(line):
    msg = pynmea2.parse(line)
    if msg.sentence_type == 'GGA':
        lat = pynmea2.dm_to_sd(msg.lat)
        lon = pynmea2.dm_to_sd(msg.lon)

        if msg.lat_dir == 'S':
            lat = lat * -1
        if msg.lon_dir == "W":
            lon = lon * -1

        message = Message(json.dumps({'gps': {'lat':lat, 'lon': lon, 'num of sats': msg.num_sats}}))
        device_client.send_message(message)
        print(f'sending telemetry: ', {lat},{lon},{msg.num_sats})

while True:
    line =serial.readline().decode('utf-8')

    while len(line) > 0:
        print_gps_data(line)
        line = serial.readline().decode('utf-8')

    time.sleep(60)