# app.py

import time
import requests
import json
import datetime as dt
import atexit

try:
    import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO module
    import board  # Import board module for pin definitions
except ImportError:
    from mock_gpio import GPIO  # Import mock GPIO module
    from mock_adafruit import DHT22, DHT11, board
    import adafruit_dht  # Import Adafruit DHT sensor library


class SensorManager:
    """Manages the sensors and controls the motor and pump based on sensor data."""

    SENSOR_PINS = [4, 17, 27]  # DHT22 on GPIO 4, DHT11 on GPIO 17, 27
    PUMP = 3  # Pin for the pump
    MOTOR = 10  # Pin for the SG90 motor

    API_URL = "https://yscyyvxduwdfjldjnwus.supabase.co"
    API_KEY = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl"
        "zY3l5dnhkdXdkZmpsZGpud3VzIiwicm9sZSI"
        "6ImFub24iLCJpYXQiOjE3MjIwNjYxMTQsImV"
        "4cCI6MjAzNzY0MjExNH0.22vV2RlrW9TU92Y"
        "79SzuOQKX8v8IISBcaHePht-43Q4"
    )
    TABLE_NAME = ["action_log", "sprinkler_get", "sprinkler_get2", "sprinkler_get3"]

    def __init__(self):
        """Initializes the SensorManager with sensors and sets up GPIO."""
        self.dht_sensors = {
            self.SENSOR_PINS[0]: adafruit_dht.DHT22(board.D4),  # DHT22 sensor
            self.SENSOR_PINS[1]: adafruit_dht.DHT11(board.D17),  # DHT11 sensor
            self.SENSOR_PINS[2]: adafruit_dht.DHT11(board.D27),  # DHT11 sensor
        }
        self.dictionary = {1: -90, 2: 0, 3: 90}  # Mapping of sensor numbers to motor angles
        self.pwm = None
        self.initialize_gpio()

    def initialize_gpio(self):
        """Initializes the GPIO settings."""
        GPIO.cleanup()  # Initialize all GPIO ports
        GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering mode
        GPIO.setup(self.SENSOR_PINS, GPIO.IN)  # Set SENSOR pins as input
        GPIO.setup(self.PUMP, GPIO.OUT)  # Set PUMP pin as output
        GPIO.setup(self.MOTOR, GPIO.OUT)  # Set MOTOR pin as output
        self.pwm = GPIO.PWM(self.MOTOR, 50)  # Set PWM for SG90 motor at 50Hz
        self.pwm.start(0)  # Start PWM with a duty cycle of 0

    def set_angle(self, angle):
        """Sets the motor to a specific angle.

        Args:
            angle (int): The angle to set the motor to.
        """
        duty = 2 + (angle / 18)  # Convert angle to duty cycle
        GPIO.output(self.MOTOR, True)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.5)
        GPIO.output(self.MOTOR, False)
        self.pwm.ChangeDutyCycle(0)  # Stop the motor by setting duty cycle to 0

    @staticmethod
    def safe_print(*args, **kwargs):
        """Prints safely, ignoring non-UTF-8 characters."""
        try:
            print(*args, **kwargs)
        except UnicodeEncodeError:
            print("Encoding error occurred while printing.")

    def send_to_supabase(self, sensor_num, temp, humi):
        """Sends sensor data to the Supabase API.

        Args:
            sensor_num (int): The sensor number.
            temp (float): The temperature data.
            humi (float): The humidity data.
        """
        url = f"{self.API_URL}/rest/v1/{self.TABLE_NAME[sensor_num]}"
        headers = {
            "Content-Type": "application/json",
            "apikey": self.API_KEY,
            "Authorization": f"Bearer {self.API_KEY}",
        }
        payload = {
            "day": str(dt.datetime.today().date()),  # Convert date to string
            "time": str(dt.datetime.today().time()),  # Convert time to string
            "temperature": temp,  # Temperature data
            "humidity": humi,  # Humidity data
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 201:
            self.safe_print(f"Data sent successfully for sensor {sensor_num + 1}")
        else:
            self.safe_print(f"Failed to send data for sensor {sensor_num + 1}: {response.text}")

    def check_sensor_conditions(self):
        """Checks each sensor for specific conditions and records which sensors meet them.

        Returns:
            list: A list of sensor numbers that met the conditions.
        """
        triggered_sensors = []
        for i, pin in enumerate(self.SENSOR_PINS):
            try:
                dht_device = self.dht_sensors[pin]
                temperature_c = dht_device.temperature
                humidity = dht_device.humidity

                if temperature_c >= 20 and humidity >= 20:
                    self.safe_print(
                        f"Sensor {i + 1} meets the condition - Temp: {temperature_c:.1f} C, Humidity: {humidity}%"
                    )
                    self.send_to_supabase(i + 1, temperature_c, humidity)
                    triggered_sensors.append(i + 1)

            except RuntimeError as error:
                # Handle sensor errors
                self.safe_print(error.args[0])
            time.sleep(2.0)
        return triggered_sensors

    def motor_angle(self, sensor_list):
        """Moves the motor to the angles corresponding to the sensors that met the conditions.

        Args:
            sensor_list (list): List of sensor numbers that met the conditions.
        """
        for sensor_number in sensor_list:
            target_angle = self.dictionary[sensor_number]  # Get the target angle corresponding to the sensor number
            self.safe_print(f"Moving motor to {target_angle}°")
            self.set_angle(target_angle)  # Move motor to the target angle

            # Move back to 0 degrees after reaching the target angle
            self.safe_print("Returning motor to 0°")
            self.set_angle(0)

    def cleanup(self):
        """Cleans up the GPIO settings."""
        self.pwm.stop()  # Stop PWM
        GPIO.cleanup()  # Clean up GPIO settings

    def run(self):
        """Runs the main loop to check sensors and control the motor and pump."""
        try:
            while True:
                result = self.check_sensor_conditions()
                if result:
                    self.motor_angle(result)
                    GPIO.output(self.PUMP, GPIO.HIGH)  # Turn pump on if condition is satisfied
                    self.safe_print(f"Sensor {result} satisfied the condition. Pump is ON.")
                    time.sleep(3)  # Keep the pump on for 3 seconds
                    GPIO.output(self.PUMP, GPIO.LOW)  # Turn pump off
                else:
                    self.safe_print("No sensor satisfied the condition. Pump remains OFF.")

                time.sleep(2.0)
        finally:
            self.cleanup()


if __name__ == "__main__":
    atexit.register(GPIO.cleanup)
    sensor_manager = SensorManager()
    sensor_manager.run()
