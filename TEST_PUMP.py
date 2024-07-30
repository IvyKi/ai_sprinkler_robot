try:
    import RPi.GPIO as GPIO     # Importing Raspberry Pi GPIO module
except ImportError:
    from mock_gpio import GPIO  # Importing mock GPIO module

import time                     # Importing time module

#GPIO.setwarnings(False)         # Disabling GPIO warnings
GPIO.setmode(GPIO.BCM)          # Setting the GPIO mode

# Setup section
PUMP_pin = 2                     # Assigning GPIO 2 to pump pin
GPIO.setup(PUMP_pin, GPIO.OUT)   # Setting pump pin as output

# Loop section
try:
    GPIO.output(PUMP_pin, GPIO.HIGH) # Turning pump on
    while True:
        time.sleep(1)                # Keeping the pump on indefinitely

# Cleanup section
finally:
    GPIO.cleanup()                   # Cleaning up GPIO
