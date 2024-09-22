"""ai_sprinkler_robot/communication.py
This module defines a class for
communication between Raspberry Pi and database or database and application.
"""


import requests
import json
import datetime as dt

API_URL = "https://yscyyvxduwdfjldjnwus.supabase.co"  # Supabase RESTful API URL
API_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl"
    "zY3l5dnhkdXdkZmpsZGpud3VzIiwicm9sZSI"
    "6ImFub24iLCJpYXQiOjE3MjIwNjYxMTQsImV"
    "4cCI6MjAzNzY0MjExNH0.22vV2RlrW9TU92Y"
    "79SzuOQKX8v8IISBcaHePht-43Q4"  # Supabase project API key
)
TABLE_NAME = ["action_log", "sprinkler_get", "sprinkler_get2", "sprinkler_get3"]


def send_to_supabase(sensor_num, temp, humi):
    url = f"{API_URL}/rest/v1/{TABLE_NAME[sensor_num]}"
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
        print(f"Data sent successfully to {TABLE_NAME[sensor_num]}")
    else:
        print(f"Failed to send data to {TABLE_NAME[sensor_num]}: {response.text}")


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
