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

# Pins for each sensor
SENSOR_PINS = [4, 17, 27]  # DHT22 on GPIO 4, DHT11 on GPIO 17, 27
PUMP = 3  # Pins for the pump
MOTOR = 10  # Pin for the SG90 motor

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
TABLE_NAME = ["action_log", "sprinkler_get", "sprinkler_get2", "sprinkler_get3"]

# Initialize each sensor
dht_sensors = {
    SENSOR_PINS[0]: adafruit_dht.DHT22(board.D4, use_pulseio=False),  # DHT22 sensor
    SENSOR_PINS[1]: adafruit_dht.DHT11(board.D17, use_pulseio=False),  # DHT11 sensor
    SENSOR_PINS[2]: adafruit_dht.DHT11(board.D27, use_pulseio=False),  # DHT11 sensor
}

# Updated motor angle dictionary (1번 -> 0도, 2번 -> 90도, 3번 -> 180도)
dictionary = {1: 0, 2: 90, 3: 180}  # Mapping of sensor numbers to motor angles

servo_min_duty = 3  # Set the minimum duty cycle to 3
servo_max_duty = 12  # Set the maximum duty cycle to 12


def initialize_gpio():
    GPIO.cleanup()  # Initialize all GPIO ports
    GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering mode
    GPIO.setup(SENSOR_PINS, GPIO.IN)  # Set SENSOR pins as input
    GPIO.setup(PUMP, GPIO.OUT)  # Set PUMP pin as output
    GPIO.setup(MOTOR, GPIO.OUT)  # Set MOTOR pin as output

    global servo
    servo = GPIO.PWM(MOTOR, 50)  # Set MOTOR pin to PWM mode with 50Hz frequency
    servo.start(0)  # Initialize PWM with a duty cycle of 0


def set_servo_angle(degree):
    """Sets the servo motor to a specific angle."""
    # Angle must be within the range of 0 to 180 degrees
    if degree > 180:
        degree = 180
    elif degree < 0:
        degree = 0

    # Convert degree to duty cycle
    duty = servo_min_duty + (degree * (servo_max_duty - servo_min_duty) / 180.0)
    servo.ChangeDutyCycle(duty)  # Change the duty cycle
    time.sleep(1)  # Give the motor time to move to the position
    servo.ChangeDutyCycle(0)  # Stop the motor


def safe_print(*args, **kwargs):
    """Prints safely, ignoring non-UTF-8 characters."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        print("Encoding error occurred while printing.")


def send_to_supabase(sensor_num: int, temp: float, humi: float):
    url = f"{API_URL}/rest/v1/{TABLE_NAME[sensor_num]}"
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
        safe_print(f"Data sent successfully for sensor {sensor_num}")
    else:
        safe_print(f"Failed to send data for sensor {sensor_num}: {response.text}")


def check_sensor_conditions():
    triggered_sensors = []
    for i, pin in enumerate(SENSOR_PINS):
        try:
            dht_device = dht_sensors[pin]
            temperature_c = dht_device.temperature
            humidity = dht_device.humidity
            send_to_supabase(i + 1, temperature_c, humidity)
            safe_print(
                    f"Sensor {i + 1} meets the condition - Temp: {temperature_c:.1f} C, Humidity: {humidity}%"
                )

            if temperature_c >= 25 and humidity >= 20:
                triggered_sensors.append(i + 1)
            else:
                pass

        except RuntimeError as error:
            # Handle sensor errors
            safe_print(error.args[0])
        time.sleep(5.0)
    return triggered_sensors


def motor_angle(sensor_list):
    # Sensor list is sorted to ensure 1, 2, 3 order
    for sensor_number in sorted(sensor_list):
        target_angle = dictionary[sensor_number]  # Get the target angle corresponding to the sensor number
        safe_print(f"Moving motor to {target_angle}° for sensor {sensor_number}")
        set_servo_angle(target_angle)  # Move motor to the target angle
        time.sleep(1)


atexit.register(GPIO.cleanup)

# Initialize GPIO
initialize_gpio()

try:
    while True:
        result = check_sensor_conditions()
        if result:
            motor_angle(result)
            GPIO.output(PUMP, GPIO.HIGH)  # Turn pump on if condition is satisfied
            safe_print(f"Sensor {result} satisfied the condition. Pump is ON.")
            time.sleep(3)  # Keep the pump on for 3 seconds
            GPIO.output(PUMP, GPIO.LOW)  # Turn pump off

        else:
            safe_print("No sensor satisfied the condition. Pump remains OFF.")

        time.sleep(1)

finally:  # This block is executed when the try block exits
    servo.stop()  # Stop PWM safely
    GPIO.cleanup()  # Clean up GPIO settings
