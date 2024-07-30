try:
    import RPi.GPIO as GPIO     # Importing Raspberry Pi GPIO module
except ImportError:
    from mock_gpio import GPIO  # Importing mock GPIO module

import time                     # Importing time module

# GPIO.set warnings(False)         # Disabling GPIO warnings
GPIO.setmode(GPIO.BCM)          # Setting the GPIO mode

# Setup section
PUMP_PIN = 2                     # Assigning GPIO 2 to pump pin
GPIO.setup(PUMP_PIN, GPIO.OUT)   # Setting pump pin as output

# Loop section
try:
    while True:
        GPIO.output(PUMP_PIN, GPIO.HIGH)  # Turning pump on
        time.sleep(1)                # Keeping the pump on indefinitely

# Cleanup section
finally:
    GPIO.cleanup()                   # Cleaning up GPIO
