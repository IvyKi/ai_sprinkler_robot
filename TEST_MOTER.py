import RPi.GPIO as GPIO
import time

# Set up GPIO pin
servo_pin = 2  # Set the control pin for the Servo motor to pin 2

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Set GPIO mode to BCM
GPIO.setup(servo_pin, GPIO.OUT)  # Set pin 2 as output

# Set up PWM
pwm = GPIO.PWM(servo_pin, 50)  # Set PWM frequency to 50Hz (SG90 servo motor uses 50Hz)
pwm.start(0)  # Start PWM with initial value 0

def set_angle(angle):
    duty = 2 + (angle / 18)  # Calculate duty cycle based on the angle
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)  # Wait for the servo to reach the position
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

try:
    while True:
        set_angle(45)   # Move the Servo motor arm to 45 degrees
        time.sleep(1)   # Wait for 1 second
        set_angle(90)   # Move the Servo motor arm to 90 degrees
        time.sleep(1)   # Wait for 1 second
        set_angle(135)  # Move the Servo motor arm to 135 degrees
        time.sleep(1)   # Wait for 1 second
        set_angle(90)   # Move the Servo motor arm to 90 degrees
        time.sleep(1)   # Wait for 1 second

finally:
    pwm.stop()  # Stop PWM
    GPIO.cleanup()  # Reset GPIO settings
