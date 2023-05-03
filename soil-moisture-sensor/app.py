from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import time
import json
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

adc = ADC()
relay = GroveRelay(5)

connection_string = "HostName=soil-moisture1.azure-devices.net;DeviceId=soil-moisture-sensor;SharedAccessKey=a5mhp4retLRrp44WG5ARYrV5+ZucHyLhHeD/Fa+gqc0="

device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

print("connecting")
device_client.connect()
print('Connected')

def handle_method_telemetry(request):
    print("Direct method received - ", request.name)

    if request.name == "relay_on":
        relay.on()
    elif request.name == "relay_off":
        relay.off()

    method_response = MethodResponse.create_from_method_request(request, 200)
    device_client.send_method_response(method_response)

device_client.on_method_request_received = handle_method_telemetry

while True:
    soil_moisture = adc.read(0)
    message = Message(json.dumps({'soil_moisture': soil_moisture}))
    device_client.send_message(message)

    time.sleep(2)