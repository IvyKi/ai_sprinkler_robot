try:
    import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO module
except ImportError:
    from mock_gpio import GPIO  # Import mock GPIO module

import setting as s
import time

servo_min_duty = 3  # Set the minimum duty cycle to 3
servo_max_duty = 12  # Set the maximum duty cycle to 12
servo = GPIO.PWM(s.MOTOR, 50)


def safe_print(*args, **kwargs):
    """Prints safely, ignoring non-UTF-8 characters."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        print("Encoding error occurred while printing.")


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
        safe_print(f"Moving motor to {target_angle}° for sensor {sensor_number}")
        set_servo_angle(target_angle)  # Move motor to the target angle
        time.sleep(1)
