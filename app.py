try:
    import RPi.GPIO as GPIO     # Import Raspberry Pi GPIO module
except ImportError:
    from mock_gpio import GPIO  # Import mock GPIO module

import time                     # Import time module
import board                    # Import board module for pin definitions
import adafruit_dht             # Import Adafruit DHT sensor library
import requests                 # Import requests module for HTTP requests
import json                     # Import json module for data formatting
import datetime as dt
from trigger import Envtrigger
GPIO.setmode(GPIO.BCM)          # Set GPIO pin numbering mode

SENSOR = 4                     # LED pin is GPIO 4 on the Raspberry Pi
GPIO.setup(SENSOR, GPIO.OUT)   # Set LED pin as output
PUMP = 3                       # Assigning GPIO 3 to pump pin
GPIO.setup(PUMP, GPIO.OUT)
API_URL = "https://yscyyvxduwdfjldjnwus.supabase.co"  # Supabase RESTful API URL
API_KEY = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl"
        "zY3l5dnhkdXdkZmpsZGpud3VzIiwicm9sZSI"
        "6ImFub24iLCJpYXQiOjE3MjIwNjYxMTQsImV"
        "4cCI6MjAzNzY0MjExNH0.22vV2RlrW9TU92Y"
        "79SzuOQKX8v8IISBcaHePht-43Q4")  # Supabase project API key
TABLE_NAME = 'sprinkler_get'  # Supabase table name
TODAY = dt.datetime.today()
DhtDevice = adafruit_dht.DHT22(board.D4)    # GPIO4 for DHT22 sensor


def initialize_gpio():
    GPIO.cleanup()              # initializing all gpio port
    GPIO.setmode(GPIO.BCM)      # Set GPIO pin numbering mod


def safe_print(*args, **kwargs):
    """Prints safely, ignoring non-UTF-8 characters."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        print("Encoding error occurred while printing.")


def send_to_supabase(temp: float, humi: float):
    url = f"{API_URL}/rest/v1/{TABLE_NAME}"
    headers = {
        'Content-Type': 'application/json',
        'apikey': API_KEY,
        'Authorization': f"Bearer {API_KEY}"
    }
    payload = {
        'day': TODAY,
        'time': TODAY.time(),
        'temperature_c': temp,
        'humidity': humi,
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        safe_print("Data sent successfully")
    else:
        safe_print(f"Failed to send data: {response.text}")


def control_sensor(temp_trigger, humi_trigger, temp_dev, humi_dev):
    if temp_trigger == "on" or humi_trigger == "on" or temp_dev == "on" or humi_dev == "on":
        GPIO.output(PUMP, GPIO.HIGH)  # on
        time.sleep(1)
        GPIO.output(SENSOR, GPIO.HIGH)  # on
        time.sleep(3)
        GPIO.output(SENSOR, GPIO.LOW)  # off
        GPIO.output(PUMP, GPIO.LOW)  # off
    else:
        GPIO.output(SENSOR, GPIO.LOW)  # sensor off
        GPIO.output(PUMP, GPIO.LOW)  # pump off


try:
    evn_trigger = Envtrigger()

    while True:
        initialize_gpio()

        try:
            temperature_c = DhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = DhtDevice.humidity
            safe_print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity))

            # Get trigger data
            temperature_trigger = "on" if temperature_c == evn_trigger.temp() else "off"
            humidity_trigger = "on" if humidity == evn_trigger.hum() else "off"
            tempdev_trigger = "on" if abs(temperature_c-evn_trigger.temp()) >= evn_trigger.temp_deviation() else "off"
            humidev_trigger = "on" if abs(humidity - evn_trigger.hum()) >= evn_trigger.hum_deviation() else "off"

            # call the function
            control_sensor(temperature_trigger, humidity_trigger, tempdev_trigger, humidev_trigger)

            # send data to Supabase
            send_to_supabase(temperature_c, humidity)

        except RuntimeError as error:
            # Handle sensor errors
            safe_print(error.args[0])
        time.sleep(2.0)

finally:                                # This block is executed when try block exits
    GPIO.cleanup()
