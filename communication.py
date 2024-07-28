"""ai_sprinkler_robot/communication.py
This module defines a class for
communication between Raspberry Pi and database or database and application.
"""

import time
import board
import datetime as dt
import adafruit_dht
import requests

SENSOR_PIN = board.D2  # Modify to the actual GPIO pin used
API_URL = "https://yscyyvxduwdfjldjnwus.supabase.co"  # Supabase RESTful API URL
API_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl"
    "zY3l5dnhkdXdkZmpsZGpud3VzIiwicm9sZSI"
    "6ImFub24iLCJpYXQiOjE3MjIwNjYxMTQsImV"
    "4cCI6MjAzNzY0MjExNH0.22vV2RlrW9TU92Y"
    "79SzuOQKX8v8IISBcaHePht-43Q4")  # Supabase project API key
BEARER_TOKEN = ""  # Optional Bearer token


class BoardComm:
    """A class to communicate with a DHT11 sensor and store data in a Supabase database.

    Attributes:
        dht_device (adafruit_dht.DHT11): The DHT11 sensor device.
        api_url (str): The Supabase RESTful API URL.
        headers (dict): The HTTP headers for the Supabase API request.
    """

    def __init__(self, sensor_pin, api_url, api_key, bearer_token=None):
        """Initializes the BoardComm class with sensor and Supabase API details.

        Args:
            sensor_pin (board.Pin): The GPIO pin to which the DHT11 sensor is connected.
            api_url (str): The URL for the Supabase REST ful API.
            api_key (str): The API key for authenticating with Supabase.
            bearer_token (str, optional): The Bearer token for additional authentication.
            Defaults to None.
        """
        self.dht_device = adafruit_dht.DHT11(sensor_pin)
        self.api_url = api_url
        self.headers = {
            "Content-Type": "application/json",
            "apikey": api_key,
        }

        if bearer_token:
            self.headers["Authorization"] = f"Bearer {bearer_token}"

    def read_sensor_data(self):
        """Reads data from the DHT11 sensor.

        Returns:
            tuple: A tuple containing the current date (datetime), time (datetime),
            temperature (float), and humidity (float), or None if reading fails.
        """
        try:
            temperature = self.dht_device.temperature
            humidity = self.dht_device.humidity
            if temperature is not None and humidity is not None:
                now = dt.datetime.now()
                current_time = now.strftime("%H:%M:%S")
                current_date = now.strftime("%Y-%m-%d")
                return current_date, current_time, temperature, humidity
            else:
                return None
        except RuntimeError as error:
            print(f"RuntimeError: {error.args[0]}")
            return None
        except Exception as error:
            self.dht_device.exit()
            raise error

    def send_data(self, current_date, current_time, temperature, humidity):
        """Sends sensor data to the Supabase database.

        Args:
            current_date (datetime): The current date in 'YYYY-MM-DD' format.
            current_time (datetime): The current time in 'HH:MM:SS' format.
            temperature (float): The temperature value from the sensor.
            humidity (float): The humidity value from the sensor.
        """
        data = {
            "day": current_date,
            "time": current_time,
            "temperature": temperature,
            "humidity": humidity
        }
        response = requests.post(self.api_url, json=data, headers=self.headers)
        if response.status_code == 201:
            print("Data successfully sent to Supabase")
        else:
            print("Failed to send data to Supabase")
            print(response.text)

    def start(self, interval=5):
        """Starts the data collection and transmission loop.

        Args:
            interval (int): The time interval (in seconds)
            between each sensor reading and data transmission.
            Defaults to 5.
        """
        while True:
            sensor_data = self.read_sensor_data()
            if sensor_data:
                current_date, current_time, temperature, humidity = sensor_data
                self.send_data(current_date, current_time, temperature, humidity)
            time.sleep(interval)


# Example usage
if __name__ == "__main__":
    board_comm = BoardComm(SENSOR_PIN, API_URL, API_KEY, BEARER_TOKEN)
    board_comm.start()
