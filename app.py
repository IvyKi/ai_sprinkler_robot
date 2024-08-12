try:
    import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO module
except ImportError:
    from mock_gpio import GPIO  # Import mock GPIO module

import time  # Import time module
import board  # Import board module for pin definitions
import adafruit_dht  # Import Adafruit DHT sensor library
import requests  # Import requests module for HTTP requests
import json  # Import json module for data formatting
import datetime as dt
import atexit

# Pin numbers for each sensor
SENSOR_PINS = [4, 17, 27, 22]  # DHT22 on GPIO 4, DHT11 on GPIO 17, 27, 22
PUMP = 3  # Pin number for the pump
MOTOR = 10  # Pin number for the motor (not used)

# Supabase RESTful API URL
API_URL = "https://yscyyvxduwdfjldjnwus.supabase.co"
# Supabase project API key
API_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl"
    "zY3l5dnhkdXdkZmpsZGpud3VzIiwicm9sZSI"
    "6ImFub24iLCJpYXQiOjE3MjIwNjYxMTQsImV"
    "4cCI6MjAzNzY0MjExNH0.22vV2RlrW9TU92Y"
    "79SzuOQKX8v8IISBcaHePht-43Q4"
)
# Supabase table names
TABLE_NAME = ["action_log", "sprinkler_get", "sprinkler_get2", "sprinkler_get3", "sprinkler_get4"]

# Initialize each sensor
dht_sensors = {
    SENSOR_PINS[0]: adafruit_dht.DHT22(board.D4),  # DHT22 sensor
    SENSOR_PINS[1]: adafruit_dht.DHT11(board.D17),  # DHT11 sensor
    SENSOR_PINS[2]: adafruit_dht.DHT11(board.D27),  # DHT11 sensor
    SENSOR_PINS[3]: adafruit_dht.DHT11(board.D22),  # DHT11 sensor
}

def initialize_gpio():
    GPIO.cleanup()  # Initialize all GPIO ports
    GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering mode
    GPIO.setup(SENSOR_PINS, GPIO.OUT)  # Set SENSOR pins as output
    GPIO.setup(PUMP, GPIO.OUT)  # Set PUMP pin as output

def safe_print(*args, **kwargs):
    """Prints safely, ignoring non-UTF-8 characters."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        print("Encoding error occurred while printing.")

def send_to_supabase(temp: float, humi: float, sensor_id: int):
    url = f"{API_URL}/rest/v1/{TABLE_NAME[sensor_id]}"
    headers = {
        "Content-Type": "application/json",
        "apikey": API_KEY,
        "Authorization": f"Bearer {API_KEY}",
    }
    payload = {
        "day": str(dt.datetime.today().date()),  # Convert date to string
        "time": str(dt.datetime.today().time()),  # Convert time to string
        "temperature": temp,  # Temperature data
        "humidity": humi,  # Humidity data
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        safe_print(f"Data sent successfully for sensor {sensor_id + 1}")
    else:
        safe_print(f"Failed to send data for sensor {sensor_id + 1}: {response.text}")

def check_sensor_conditions():
    for i, pin in enumerate(SENSOR_PINS):
        try:
            dhtDevice = dht_sensors[pin]
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity
            
            if temperature_c >= 20 and humidity >= 20:
                safe_print(
                    f"Sensor {i + 1} meets the condition - Temp: {temperature_c:.1f} C, Humidity: {humidity}%"
                )
                send_to_supabase(temperature_c, humidity, i)
                return i + 1  # Return the sensor number that meets the condition

        except RuntimeError as error:
            # Handle sensor errors
            safe_print(error.args[0])
        time.sleep(2.0)

    return None  # Return None if no sensor meets the condition

# Ensure cleanup is called on script exit
atexit.register(GPIO.cleanup)

# Initialize GPIO
initialize_gpio()

try:
    while True:
        result = check_sensor_conditions()
        if result is not None:
            GPIO.output(PUMP, GPIO.HIGH)  # Turn pump on if condition is satisfied
            safe_print(f"Sensor {result} satisfied the condition. Pump is ON.")
            time.sleep(3)  # Keep the pump on for 3 seconds
            GPIO.output(PUMP, GPIO.LOW)  # Turn pump off
        else:
            safe_print("No sensor satisfied the condition. Pump remains OFF.")

        time.sleep(2.0)

finally:  # This block is executed when the try block exits
    GPIO.cleanup()  # Clean up GPIO settings
