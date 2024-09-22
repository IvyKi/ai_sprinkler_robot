from supabase import create_client, Client
from trigger import predict_weather, predict_probability
import datetime as dt

API_URL = "https://yscyyvxduwdfjldjnwus.supabase.co"
API_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl"
    "zY3l5dnhkdXdkZmpsZGpud3VzIiwicm9sZSI"
    "6ImFub24iLCJpYXQiOjE3MjIwNjYxMTQsImV"
    "4cCI6MjAzNzY0MjExNH0.22vV2RlrW9TU92Y"
    "79SzuOQKX8v8IISBcaHePht-43Q4")
TABLE = ["action_log", "sprinkler_get", "sprinkler_get2", "sprinkler_get3", "sprinkler_get4"]
PORT_NUM = [3, 4, 17, 27, 22]   # pump: 3, sensor: 4, 17, 27, 22
TODAY = dt.datetime.today()
SUPABASE: Client = create_client(API_URL, API_KEY)
FILE_PATH = ['data001.xlsx', 'data002.xlsx']


def load_data(sensor_num):
    response = SUPABASE.table(TABLE[sensor_num]).select("*").execute()
    data = response.data

    day = [row["day"] for row in data]
    times = [row["time"] for row in data]
    time = [time.split('.')[0] for time in times]
    temp = [row["temperature"] for row in data]
    hum = [row["humidity"] for row in data]

    return day, time, temp, hum


def extract_day(day):
    date_list = day
    month_day_list = [[int(dt.datetime.strptime(date, "%Y-%m-%d").month),
                       int(dt.datetime.strptime(date, "%Y-%m-%d").day)]
                      for date in date_list]

    return month_day_list


def compare_probability(a):
    probability = predict_probability(FILE_PATH[0], a[0], a[1])

    if probability >= 75.00:
        return True
    else:
        return False


def compare_weather(a, temp, hum):
    trig_temp, trig_hum = False, False
    result = []

    temperature, humidity = predict_weather(FILE_PATH[1], a[0], a[1])
    if temp >= temperature:
        trig_temp = True

    if hum <= humidity:
        trig_hum = True

    result.append(trig_temp)
    result.append(trig_hum)

    return result


if __name__ == '__main__':
    DAY, TIME, TEMP, HUM = load_data(1)

    m_d_list = extract_day(DAY)

    control_day = []
    control_weather = []
    for i in range(len(DAY)):
        control_day.append(compare_probability(m_d_list[i]))
        control_weather.append(compare_weather(m_d_list[i], TEMP[i], HUM[i]))

    print(control_day)
    print(control_weather)
