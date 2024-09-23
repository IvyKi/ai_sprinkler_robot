try:
    import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO module
except ImportError:
    from mock_gpio import GPIO  # Import mock GPIO module

import time
import setting as s
import atexit
import communication as comm
import angle


def initialize_gpio():
    GPIO.cleanup()  # Initialize all GPIO ports
    GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering mode
    GPIO.setup(s.SENSOR_PINS, GPIO.IN)  # Set SENSOR pins as input
    GPIO.setup(s.PUMP, GPIO.OUT)  # Set PUMP pin as output
    GPIO.setup(s.MOTOR, GPIO.OUT)  # Set MOTOR pin as output

    angle.servo.start(0)  # Initialize PWM with a duty cycle of 0


atexit.register(GPIO.cleanup)

# Initialize GPIO
initialize_gpio()

try:
    while True:
        result = comm.check_sensor_conditions()
        action = comm.read_from_supabase()
        if result:
            angle.motor_angle(result)
            GPIO.output(s.PUMP, GPIO.HIGH)  # Turn pump on if condition is satisfied
            comm.safe_print(f"Sensor {result} satisfied the condition. Pump is ON.")
            time.sleep(3)  # Keep the pump on for 3 seconds
            GPIO.output(s.PUMP, GPIO.LOW)  # Turn pump off

        elif action:
            angle.motor_angle(action)
            GPIO.output(s.PUMP, GPIO.HIGH)  # Turn pump on if condition is satisfied
            comm.safe_print(f"Sensor {action} satisfied the condition. Pump is ON.")
            time.sleep(3)  # Keep the pump on for 3 seconds
            GPIO.output(s.PUMP, GPIO.LOW)  # Turn pump off

        else:
            comm.safe_print("No sensor satisfied the condition. Pump remains OFF.")

        time.sleep(1)

finally:  # This block is executed when the try block exits
    angle.servo.stop()  # Stop PWM safely
    GPIO.cleanup()  # Clean up GPIO settings
