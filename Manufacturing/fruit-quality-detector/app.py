from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import io
from counterfit_shims_picamera import PiCamera
import requests

camera = PiCamera()
camera.resolution = (640, 480)
camera.rotation = 0

image = io.BytesIO()
camera.capture(image, 'jpeg')
image.seek(0)

with open('image.jpg', 'wb') as image_file:
    image_file.write(image.read())

prediction_url = 'http://192.168.137.251/image' # Replace with your IP address
headers = {
    'Content-Type' : 'application/octet-stream'
}
image.seek(0)
response = requests.post(prediction_url, headers=headers, data=image)
results = response.json()

for prediction in results['predictions']:
    print(f'{prediction["tagName"]}:\t{prediction["probability"] * 100:.2f}%')