import requests
import setting as s
import json
import time


def safe_print(*args, **kwargs):
    """Prints safely, ignoring non-UTF-8 characters."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        print("Encoding error occurred while printing.")


def send_to_supabase(sensor_num: int, temp: float, humi: float, trig: bool):
    url = f"{s.API_URL}/rest/v1/{s.TABLE[sensor_num]}"
    headers = {
        "Content-Type": "application/json",
        "apikey": s.API_KEY,
        "Authorization": f"Bearer {s.API_KEY}",
    }
    payload = {
        "day": str(s.TODAY.date()),  # Convert date to string
        "time": str(s.TODAY.time()),  # Convert time to string
        "temperature": temp,  # Temperature data
        "humidity": humi,  # Humidity data
        "trigger": trig

    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        safe_print(f"Data sent successfully for sensor {sensor_num}")
    else:
        safe_print(f"Failed to send data for sensor {sensor_num}: {response.text}")


def read_from_supabase():
    action_sensors = []

    url = f"{s.API_URL}/rest/v1/{s.TABLE[0]}"
    headers = {
        "apikey": s.API_KEY,  # Assuming your API key is stored in s.API_KEY
        "Authorization": f"Bearer {s.API_KEY}",
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        return []

    data = response.json()
    sensor_initials = {
        'sensor_A': 1,
        'sensor_B': 2,
        'sensor_C': 3
    }

    for row in data:
        for sensor, initial in sensor_initials.items():
            if row.get(sensor):
                action_sensors.append(initial)

    return action_sensors


def check_sensor_conditions():
    triggered_sensors = []

    for i, pin in enumerate(s.SENSOR_PINS):
        try:
            dht_device = s.DHT_SENSORS[pin]
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            safe_print(
                    f"Sensor {i + 1} meets the condition - Temp: {temperature:.1f} C, Humidity: {humidity}%"
                )
            trigger = False
            if temperature >= s.PRE_T and humidity >= s.PRE_H:
                triggered_sensors.append(i + 1)
                trigger = True
            send_to_supabase(i + 1, temperature, humidity, trigger)

        except RuntimeError as error:
            # Handle sensor errors
            safe_print(error.args[0])
        time.sleep(5.0)

    return triggered_sensors
