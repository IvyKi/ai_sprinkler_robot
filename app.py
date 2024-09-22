try:
    import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO module
except ImportError:
    from mock_gpio import GPIO  # Import mock GPIO module

import time  # Import time module
import requests  # Import requests module for HTTP requests
import json  # Import json module for data formatting
import datetime as dt
import setting as s
import atexit
from trigger import predict_weather, predict_probability


servo_min_duty = 3  # Set the minimum duty cycle to 3
servo_max_duty = 12  # Set the maximum duty cycle to 12
servo = GPIO.PWM(s.MOTOR, 50)
probability = predict_probability(s.FILE_PATH[0], int(s.TODAY.month), int(s.TODAY.day))
pre_t, pre_h = predict_weather(s.FILE_PATH[1], int(s.TODAY.month), int(s.TODAY.day))


def initialize_gpio():
    GPIO.cleanup()  # Initialize all GPIO ports
    GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering mode
    GPIO.setup(s.SENSOR_PINS, GPIO.IN)  # Set SENSOR pins as input
    GPIO.setup(s.PUMP, GPIO.OUT)  # Set PUMP pin as output
    GPIO.setup(s.MOTOR, GPIO.OUT)  # Set MOTOR pin as output

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
    url = f"{s.API_URL}/rest/v1/{s.TABLE[sensor_num]}"
    headers = {
        "Content-Type": "application/json",
        "apikey": s.API_KEY,
        "Authorization": f"Bearer {s.API_KEY}",
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

    for i, pin in enumerate(s.SENSOR_PINS):
        try:
            dht_device = s.DHT_SENSORS[pin]
            temperature_c = dht_device.temperature
            humidity = dht_device.humidity
            send_to_supabase(i + 1, temperature_c, humidity)
            safe_print(
                    f"Sensor {i + 1} meets the condition - Temp: {temperature_c:.1f} C, Humidity: {humidity}%"
                )

            if temperature_c >= pre_t and humidity >= pre_h:
                triggered_sensors.append(i + 1)

        except RuntimeError as error:
            # Handle sensor errors
            safe_print(error.args[0])
        time.sleep(5.0)
    return triggered_sensors


def motor_angle(sensor_list):
    # Sensor list is sorted to ensure 1, 2, 3 order
    for sensor_number in sorted(sensor_list):
        target_angle = s.ANGLE[sensor_number]  # Get the target angle corresponding to the sensor number
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
            GPIO.output(s.PUMP, GPIO.HIGH)  # Turn pump on if condition is satisfied
            safe_print(f"Sensor {result} satisfied the condition. Pump is ON.")
            time.sleep(3)  # Keep the pump on for 3 seconds
            GPIO.output(s.PUMP, GPIO.LOW)  # Turn pump off

        else:
            safe_print("No sensor satisfied the condition. Pump remains OFF.")

        time.sleep(1)

finally:  # This block is executed when the try block exits
    servo.stop()  # Stop PWM safely
    GPIO.cleanup()  # Clean up GPIO settings
