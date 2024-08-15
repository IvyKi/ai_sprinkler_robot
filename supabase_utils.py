import requests
import json
import datetime as dt

# Supabase RESTful API URL
API_URL = "https://yscyyvxduwdfjldjnwus.supabase.co"
API_KEY = "YOUR_SUPABASE_API_KEY"
TABLE_NAME = ["action_log", "sprinkler_get", "sprinkler_get2", "sprinkler_get3", "sprinkler_get4"]


def send_to_supabase(temp: float, humi: float, sensor_id: int):
    url = f"{API_URL}/rest/v1/{TABLE_NAME[sensor_id]}"
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
        print(f"Data sent successfully for sensor {sensor_id + 1}")
    else:
        print(f"Failed to send data for sensor {sensor_id + 1}: {response.text}")
