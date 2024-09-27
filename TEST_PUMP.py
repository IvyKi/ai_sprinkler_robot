import RPi.GPIO as GPIO
import time

# GPIO pin setup
PUMP_PIN = 2

# GPIO initialization
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PUMP_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(PUMP_PIN, GPIO.HIGH)  # Turning pump on
        time.sleep(5)                     # Keep the pump on for 5 seconds
        GPIO.output(PUMP_PIN, GPIO.LOW)   # Turning pump off
        time.sleep(1)                     # Keep the pump off for 1 second

finally:
    # GPIO cleanup
    GPIO.cleanup()
    print("GPIO cleanup complete")
