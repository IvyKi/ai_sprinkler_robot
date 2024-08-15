import time
import board
import adafruit_dht
from supabase_utils import send_to_supabase

# Pins for each sensor
SENSOR_PINS = [4, 17, 27, 22]

# Initialize each sensor
dht_sensors = {
    SENSOR_PINS[0]: adafruit_dht.DHT22(board.D4),
    SENSOR_PINS[1]: adafruit_dht.DHT11(board.D17),
    SENSOR_PINS[2]: adafruit_dht.DHT11(board.D27),
    SENSOR_PINS[3]: adafruit_dht.DHT11(board.D22),
}


def check_sensor_conditions():
    triggered_sensors = []
    for i, pin in enumerate(SENSOR_PINS):
        try:
            dht_device = dht_sensors[pin]
            temperature_c = dht_device.temperature
            humidity = dht_device.humidity

            if temperature_c >= 20 and humidity >= 20:
                print(
                    f"Sensor {i + 1} meets the condition - Temp: {temperature_c:.1f} C, Humidity: {humidity}%"
                )
                send_to_supabase(temperature_c, humidity, i)
                triggered_sensors.append(i + 1)

        except RuntimeError as error:
            print(error.args[0])
        time.sleep(2.0)
    return triggered_sensors
