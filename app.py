import time
import atexit
from gpio_utils import initialize_gpio, cleanup_gpio
from sensor_utils import check_sensor_conditions
from motor_utils import motor_angle
try:
    import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO module
except ImportError:
    from mock_gpio import GPIO  # Import mock GPIO module

# Ensure cleanup is called on script exit
atexit.register(cleanup_gpio)

# Initialize GPIO
initialize_gpio()

try:
    while True:
        result = check_sensor_conditions()
        if result:
            motor_angle(result)
            GPIO.output(3, GPIO.HIGH)  # Turn pump on if condition is satisfied
            print(f"Sensor {result} satisfied the condition. Pump is ON.")
            time.sleep(3)  # Keep the pump on for 3 seconds
            GPIO.output(3, GPIO.LOW)  # Turn pump off
        else:
            print("No sensor satisfied the condition. Pump remains OFF.")

        time.sleep(2.0)

finally:
    cleanup_gpio()
