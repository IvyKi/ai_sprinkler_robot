import time
import board
import adafruit_dht
from supabase_utils import send_to_supabase, log_action

# DHT SENSOR PIN LIST
SENSOR_PINS = [4, 17, 27, 22]

# Environment trigger
TEMP_TRIGGER = 20.0
HUM_TRIGGER = 45.0

# initialize sensor
dht_sensors = {
    SENSOR_PINS[0]: adafruit_dht.DHT22(board.D4),
    SENSOR_PINS[1]: adafruit_dht.DHT11(board.D17),
    SENSOR_PINS[2]: adafruit_dht.DHT11(board.D27),
    SENSOR_PINS[3]: adafruit_dht.DHT11(board.D22),
}


def check_sensor():
    triggered_sensors = []
    for i, pin in enumerate(SENSOR_PINS):
        try:
            dht_device = dht_sensors[pin]
            temperature_c = dht_device.temperature
            humidity = dht_device.humidity

            if temperature_c is not None and humidity is not None:
                table_name = f"sprinkler_get{i + 1}"
                send_to_supabase(table_name, temperature_c, humidity)

                if temperature_c < TEMP_TRIGGER or humidity < HUM_TRIGGER:
                    log_action(temperature_c, humidity, i + 1)
                    triggered_sensors.append(i + 1)

        except RuntimeError as error:
            print(f"Sensor {i + 1} error: {error.args[0]}")
        time.sleep(2.0)
    return triggered_sensors


if __name__ == "__main__":
    sensor = check_sensor()
    print(sensor)