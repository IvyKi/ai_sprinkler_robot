try:
    import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO module
except ImportError:
    from mock_gpio import GPIO  # Import mock GPIO module

SENSOR_PINS = [4, 17, 27, 22]  # DHT sensor pin
PUMP_PIN = 3  # water pump pin
MOTOR_PIN = 10


def initialize_gpio():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SENSOR_PINS, GPIO.IN)  # DHT 센서 핀 입력 모드로 설정
    GPIO.setup(PUMP_PIN, GPIO.OUT)  # 펌프 핀 출력 모드로 설정


def cleanup_gpio():
    GPIO.cleanup()
