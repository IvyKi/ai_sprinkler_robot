try:
    import RPi.GPIO as GPIO     # Import Raspberry Pi GPIO module
except ImportError:
    from mock_gpio import GPIO  # Import mock GPIO module

import time                     # Import time module
import board                    # Import board module for pin definitions
import adafruit_dht             # Import Adafruit DHT sensor library
from communication import BoardComm
GPIO.setmode(GPIO.BCM)          # Set GPIO pin numbering mode

SENSOR = 4                     # LED pin is GPIO 2 on the Raspberry Pi
GPIO.setup(SENSOR, GPIO.OUT)   # Set LED pin as output
PUMP = 3                     # Assigning GPIO 2 to pump pin
GPIO.setup(PUMP, GPIO.OUT)
API_URL = "https://yscyyvxduwdfjldjnwus.supabase.co"  # Supabase RESTful API URL
API_KEY = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl"
        "zY3l5dnhkdXdkZmpsZGpud3VzIiwicm9sZSI"
        "6ImFub24iLCJpYXQiOjE3MjIwNjYxMTQsImV"
        "4cCI6MjAzNzY0MjExNH0.22vV2RlrW9TU92Y"
        "79SzuOQKX8v8IISBcaHePht-43Q4")  # Supabase project API key
BEARER_TOKEN = ""  # Optional Bearer token

dhtDevice = adafruit_dht.DHT22(board.D4)    # GPIO2


def safe_print(*args, **kwargs):
    """Prints safely, ignoring non-UTF-8 characters."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        print("Encoding error occurred while printing.")


try:
    while True:
        GPIO.output(PUMP, GPIO.HIGH)  # Turning pump on
        time.sleep(1)
        GPIO.output(SENSOR, GPIO.HIGH)  # Turning pump on
        time.sleep(5)                     # Keep the pump on for 5 seconds
        GPIO.output(SENSOR, GPIO.LOW)   # Turning pump off
        time.sleep(1)

        try:
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            safe_print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity))
            board_comm = BoardComm(board.D15, API_URL, API_KEY, BEARER_TOKEN)
            board_comm.start()

        except RuntimeError as error:
            # Handle sensor errors
            safe_print(error.args[0])
        time.sleep(4.0)

finally:                                # This block is executed when try block exits
    GPIO.cleanup()
