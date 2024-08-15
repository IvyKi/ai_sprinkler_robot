try:
    import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO module
except ImportError:
    from mock_gpio import GPIO  # Import mock GPIO module

# Pins for each sensor
SENSOR_PINS = [4, 17, 27, 22]
PUMP = 3
MOTOR = 10


def initialize_gpio():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SENSOR_PINS, GPIO.OUT)
    GPIO.setup(PUMP, GPIO.OUT)
    GPIO.setup(MOTOR, GPIO.OUT)


def cleanup_gpio():
    GPIO.cleanup()
