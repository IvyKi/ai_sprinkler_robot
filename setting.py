from supabase import create_client, Client
import datetime as dt
import board  # Import board module for pin definitions
import adafruit_dht  # Import Adafruit DHT sensor library


API_URL = "https://yscyyvxduwdfjldjnwus.supabase.co"
API_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl"
    "zY3l5dnhkdXdkZmpsZGpud3VzIiwicm9sZSI"
    "6ImFub24iLCJpYXQiOjE3MjIwNjYxMTQsImV"
    "4cCI6MjAzNzY0MjExNH0.22vV2RlrW9TU92Y"
    "79SzuOQKX8v8IISBcaHePht-43Q4")
TABLE = ["action_log", "sprinkler_get1", "sprinkler_get2", "sprinkler_get3", "sprinkler_get4"]
TODAY = dt.datetime.today()
SUPABASE: Client = create_client(API_URL, API_KEY)
FILE_PATH = ['data001.xlsx', 'data002.xlsx']


SENSOR_PINS = [4, 17, 27]  # DHT22 on GPIO 4, DHT11 on GPIO 17, 27
PUMP = 3  # Pins for the pump
MOTOR = 10  # Pin for the SG90 motor
PORT_NUM = [3, 4, 17, 27, 22]   # pump: 3, sensor: 4, 17, 27, 22
DHT_SENSORS = {
    SENSOR_PINS[0]: adafruit_dht.DHT22(board.D4, use_pulseio=False),  # DHT22 sensor
    SENSOR_PINS[1]: adafruit_dht.DHT11(board.D17, use_pulseio=False),  # DHT11 sensor
    SENSOR_PINS[2]: adafruit_dht.DHT11(board.D27, use_pulseio=False),  # DHT11 sensor
}
ANGLE = {1: 0, 2: 90, 3: 180}  # Mapping of sensor numbers to motor angles
