try:
    import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO module
except ImportError:
    from mock_gpio import GPIO  # Import mock GPIO module

import time  # Import time module
import setting as s
import atexit
from trigger import predict_weather, predict_probability
import communication as comm


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


def motor_angle(sensor_list):
    # Sensor list is sorted to ensure 1, 2, 3 order
    for sensor_number in sorted(sensor_list):
        target_angle = s.ANGLE[sensor_number]  # Get the target angle corresponding to the sensor number
        comm.safe_print(f"Moving motor to {target_angle}° for sensor {sensor_number}")
        set_servo_angle(target_angle)  # Move motor to the target angle
        time.sleep(1)


atexit.register(GPIO.cleanup)

# Initialize GPIO
initialize_gpio()

try:
    while True:
        result = comm.check_sensor_conditions()
        action = comm.read_from_supabase()
        if result:
            motor_angle(result)
            GPIO.output(s.PUMP, GPIO.HIGH)  # Turn pump on if condition is satisfied
            comm.safe_print(f"Sensor {result} satisfied the condition. Pump is ON.")
            time.sleep(3)  # Keep the pump on for 3 seconds
            GPIO.output(s.PUMP, GPIO.LOW)  # Turn pump off

        elif action:
            motor_angle(action)
            GPIO.output(s.PUMP, GPIO.HIGH)  # Turn pump on if condition is satisfied
            comm.safe_print(f"Sensor {action} satisfied the condition. Pump is ON.")
            time.sleep(3)  # Keep the pump on for 3 seconds
            GPIO.output(s.PUMP, GPIO.LOW)  # Turn pump off

        else:
            comm.safe_print("No sensor satisfied the condition. Pump remains OFF.")

        time.sleep(1)

finally:  # This block is executed when the try block exits
    servo.stop()  # Stop PWM safely
    GPIO.cleanup()  # Clean up GPIO settings
