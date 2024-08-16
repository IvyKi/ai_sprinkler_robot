import requests
import json
import datetime as dt

API_URL = "aaa"
API_KEY = "bbb"
TABLE_NAME = ["action_log", "sprinkler_get", "sprinkler_get2", "sprinkler_get3", "sprinkler_get4"]


def send_to_supabase(table_name, temp, humi):
    url = f"{API_URL}/rest/v1/{table_name}"
    headers = {
        "Content-Type": "application/json",
        "apikey": API_KEY,
        "Authorization": f"Bearer {API_KEY}",
    }
    payload = {
        "day": str(dt.datetime.today().date()),
        "time": str(dt.datetime.today().time()),
        "temperature": temp,
        "humidity": humi,
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        print(f"Data sent successfully to {table_name}")
    else:
        print(f"Failed to send data to {table_name}: {response.text}")


def log_action(temp, humi, sensor_num):
    url = f"{API_URL}/rest/v1/action_log"
    headers = {
        "Content-Type": "application/json",
        "apikey": API_KEY,
        "Authorization": f"Bearer {API_KEY}",
    }
    payload = {
        "day": str(dt.datetime.today().date()),
        "time": str(dt.datetime.today().time()),
        "temperature": temp,
        "humidity": humi,
        "sensor_num": sensor_num,
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        print(f"Action logged for sensor {sensor_num}")
    else:
        print(f"Failed to log action for sensor {sensor_num}: {response.text}")
