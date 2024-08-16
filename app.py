import time
import atexit
from gpio_utils import initialize_gpio, cleanup_gpio, PUMP_PIN
from sensor_utils import check_sensor
from motor_utils import motor_angle
try:
    import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO module
except ImportError:
    from mock_gpio import GPIO  # Import mock GPIO module

# gpio initialize
atexit.register(cleanup_gpio)
initialize_gpio()

try:
    while True:
        triggered_sensors = check_sensor()
        if triggered_sensors:
            # motor angle
            GPIO.output(PUMP_PIN, GPIO.HIGH)  # pump on
            print(f"Sensors {triggered_sensors} triggered the pump. Pump is ON.")
            time.sleep(3)  # 3 seconds working
            GPIO.output(PUMP_PIN, GPIO.LOW)  # pump off
        else:
            print("No sensors triggered. Pump remains OFF.")

        time.sleep(2.0)  # wait for 2 seconds

finally:
    cleanup_gpio()
