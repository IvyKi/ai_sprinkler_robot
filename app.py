import time
import atexit
from gpio_utils import initialize_gpio, cleanup_gpio, PUMP_PIN
from sensor_utils import check_sensor
from motor_utils import motor_angle
try:
    import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO module
except ImportError:
    from mock_gpio import GPIO  # Import mock GPIO module

# GPIO 초기화 및 클린업 설정
atexit.register(cleanup_gpio)
initialize_gpio()

try:
    while True:
        triggered_sensors = check_sensor()
        if triggered_sensors:
            GPIO.output(PUMP_PIN, GPIO.HIGH)  # 펌프 켜기
            print(f"Sensors {triggered_sensors} triggered the pump. Pump is ON.")
            time.sleep(3)  # 펌프 3초간 동작
            GPIO.output(PUMP_PIN, GPIO.LOW)  # 펌프 끄기
        else:
            print("No sensors triggered. Pump remains OFF.")

        time.sleep(2.0)  # 다음 루프 전 잠깐 대기

finally:
    cleanup_gpio()
