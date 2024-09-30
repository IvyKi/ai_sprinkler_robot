try:
    import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO module
except ImportError:
    from mock_gpio import GPIO  # Import mock GPIO module

import time  # Import time module
import board  # Import board module for pin definitions
import adafruit_dht  # Import Adafruit DHT sensor library
import datetime as dt
import atexit
import pandas as pd
import requests
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


class PredictWeather:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.average_data = None

    def load_data(self):
        """Load the data from the Excel file."""
        self.data = pd.read_excel(self.file_path)

    def fill_missing_values(self):
        """Fill missing values in temperature and humidity columns with their respective mean values."""
        self.data['Temperature'] = self.data['Temperature'].fillna(self.data['Temperature'].mean())
        self.data['Humidity'] = self.data['Humidity'].fillna(self.data['Humidity'].mean())

    def calculate_average(self):
        """Group the data by 'Month' and 'Day' and calculate the mean temperature and humidity."""
        self.average_data = self.data.groupby(['Month', 'Day'], as_index=False).agg(
            {'Temperature': 'mean', 'Humidity': 'mean'})

    def get_avg_temp_humidity(self, month, day):
        """Return the average temperature and humidity for a given month and day."""
        if self.average_data is None:
            raise ValueError("Average data not calculated. Please run calculate_average() first.")

        result = self.average_data[(self.average_data['Month'] == month) & (self.average_data['Day'] == day)]
        if not result.empty:
            avg_temp = result['Temperature'].values[0]
            avg_humidity = result['Humidity'].values[0]
            return avg_temp, avg_humidity
        else:
            return None, None  # Return None if the date is not found in the data

    def predict_today_weather(self, month, day):
        """Predict the average temperature and humidity for today's date."""
        return self.get_avg_temp_humidity(month, day)


class PredictProbability:
    def __init__(self, data_path):
        self.data_path = data_path
        self.fire_data = None
        self.all_dates = None
        self.x = None
        self.x_train = None
        self.x_test = None
        self.y = None
        self.y_pred = None
        self.y_train = None
        self.y_test = None
        self.probability = 0
        self.model = None

    def load_data(self):
        """Load the fire data from an Excel file."""
        self.fire_data = pd.read_excel(self.data_path)
        self.fire_data['Fire_Occurred'] = 1

    def generate_all_dates(self):
        """Generate all valid dates for a year and merge with fire data."""
        valid_dates = []
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    pd.Timestamp(f'2020-{month}-{day}')
                    valid_dates.append((month, day))
                except ValueError:
                    continue

        all_dates_df = pd.DataFrame(valid_dates, columns=['Month', 'Day'])
        self.all_dates = all_dates_df.merge(
            self.fire_data[['Month', 'Day', 'Fire_Occurred']],
            on=['Month', 'Day'],
            how='left', validate="many_to_many").fillna(0)

    def prepare_data(self):
        """Prepare the features and target variable."""
        self.x = self.all_dates[['Month', 'Day']].values
        self.y = self.all_dates['Fire_Occurred'].values
        return train_test_split(self.x, self.y, test_size=0.2, random_state=42)

    def train_model(self):
        """Train the logistic regression model.

            print(f"Model Accuracy: {accuracy * 100:.2f}%")
            print("Classification Report:\n", report)
        """
        self.x_train, self.x_test, self.y_train, self.y_test = self.prepare_data()
        self.model = LogisticRegression(random_state=42)
        self.model.fit(self.x_train, self.y_train)

        # Evaluate the model
        self.y_pred = self.model.predict(self.x_test)
        accuracy = accuracy_score(self.y_test, self.y_pred)
        report = classification_report(self.y_test, self.y_pred)

        return accuracy, report

    def predict_fire_probability(self, month, day):
        """Predict the probability of fire occurrence for a given date."""
        if not self.model:
            raise ValueError("Model is not trained yet. Call train_model() first.")

        self.probability = self.model.predict_proba([[month, day]])[0][1]
        return self.probability * 100

    def predict_today_fire_probability(self, month, day):
        """Predict the probability of fire occurrence for today's date."""
        return self.predict_fire_probability(month, day)


def set_servo_angle(degree):
    """Sets the servo motor to a specific angle."""
    # Ensure the angle is within the range of 0 to 180 degrees
    if degree > 180:
        degree = 180
    elif degree < 0:
        degree = 0

    # Convert degree to duty cycle
    duty = servo_min_duty + (degree * (servo_max_duty - servo_min_duty) / 180.0)
    servo.ChangeDutyCycle(duty)  # Change the duty cycle
    time.sleep(1)  # Give the motor time to move to the position
    servo.ChangeDutyCycle(0)  # Stop the motor


def safe_print(*args, **kwargs):
    """Prints safely, ignoring non-UTF-8 characters."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        print("Encoding error occurred while printing.")


def predict_probability(file_path, month, day):
    ml_a = PredictProbability(file_path)
    ml_a.load_data()
    ml_a.generate_all_dates()
    ml_a.train_model()
    prob = ml_a.predict_today_fire_probability(month, day)

    return round(float(prob), 2)


def predict_weather(file_path, month, day):
    ml_b = PredictWeather(file_path)
    ml_b.load_data()
    ml_b.fill_missing_values()
    ml_b.calculate_average()
    t, h = ml_b.predict_today_weather(month, day)

    return round(float(t), 2), round(float(h), 2)


def check_sensor_conditions():
    weather_triggered_sensors = []
    day_triggered_sensors = []
    for i, pins in enumerate(SENSOR_PINS):
        try:
            dht_device = dht_sensors[pins]
            temperature_c = dht_device.temperature
            humidity = dht_device.humidity
            trigger = False

            safe_print(
                    f"Sensor {i + 1} meets the condition - Temp: {temperature_c:.1f} C, Humidity: {humidity}%"
            )
            if temperature_c >= pre_t and humidity >= pre_h:
                weather_triggered_sensors.append(i + 1)
                trigger = True
            elif probability >= 89:
                day_triggered_sensors.append(i + 1)
                trigger = True

            send_to_supabase(i + 1, temperature_c, humidity, trigger)

        except RuntimeError as error:
            # Handle sensor errors
            safe_print(error.args[0])
        time.sleep(5.0)
    #
    # try:
    #     dht_device1 = dht_sensors[0]
    #     temp1 = dht_device1.temperature
    #     hum1 = dht_device1.humidity
    #     trigger1 = False
    #     safe_print(f"Sensor 1 meents the condition - Temp: {temp1:.1f} C, Humidity: {hum1:.1f}")
    #     if temp1 >= pre_t and hum1 >= pre_h:
    #         weather_triggered_sensors.append(1)
    #         trigger1 = True
    #     elif probability >= 89:
    #         day_triggered_sensors.append(1)
    #         trigger1 = True
    #     else:
    #         pass
    #     send_to_supabase(1, temp1, hum1, trigger1)
    #     time.sleep(5.0)
    #
    #     dht_device2 = dht_sensors[1]
    #     temp2 = dht_device2.temperature
    #     hum2 = dht_device2.humidity
    #     trigger2 = False
    #     safe_print(f"Sensor 1 meents the condition - Temp: {temp2:.1f} C, Humidity: {hum2:.1f}")
    #     if temp2 >= pre_t and hum2 >= pre_h:
    #         weather_triggered_sensors.append(2)
    #         trigger2 = True
    #     elif probability >= 89:
    #         day_triggered_sensors.append(2)
    #         trigger2 = True
    #     else:
    #         pass
    #     send_to_supabase(2, temp2, hum2, trigger2)
    #     time.sleep(5.0)
    #
    #     dht_device3 = dht_sensors[2]
    #     temp3 = dht_device3.temperature
    #     hum3 = dht_device3.humidity
    #     trigger3 = False
    #     safe_print(f"Sensor 1 meents the condition - Temp: {temp3:.1f} C, Humidity: {hum3:.1f}")
    #     if temp3 >= pre_t and hum3 >= pre_h:
    #         weather_triggered_sensors.append(3)
    #         trigger3 = True
    #     elif probability >= 89:
    #         day_triggered_sensors.append(3)
    #         trigger3 = True
    #     else:
    #         pass
    #     send_to_supabase(3, temp3, hum3, trigger3)
    #     time.sleep(5.0)
    #
    # except RuntimeError as error:
    #     safe_print(error.args[0])
    # time.sleep(5.0)

    return weather_triggered_sensors, day_triggered_sensors


def send_to_supabase(sensor_num, temp, humi, trig):
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
        "trigger": trig,
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        print(f"Data sent successfully to {TABLE_NAME[sensor_num]}")
    else:
        print(f"Failed to send data to {TABLE_NAME[sensor_num]}: {response.text}")


def motor_angle(sensor_list):
    # Sort the sensor list to ensure it processes in the order 1, 2, 3
    for sensor_number in sorted(sensor_list):
        target_angle = dictionary[sensor_number]  # Get the target angle corresponding to the sensor number
        safe_print(f"Moving motor to {target_angle}° for sensor {sensor_number}")
        set_servo_angle(target_angle)  # Move motor to the target angle
        time.sleep(1)


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


def read_from_supabase():
    action_sensors = []

    url = f"{API_URL}/rest/v1/{TABLE_NAME[0]}"
    headers = {
        "apikey": API_KEY,  # Assuming your API key is stored in s.API_KEY
        "Authorization": f"Bearer {API_KEY}",
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


#####
# Pins for each sensor
SENSOR_PINS = [17, 27, 22]  # DHT22 on GPIO 4, DHT11 on GPIO 17, 27
PUMP = 3  # Pin for the pump
MOTOR = 10  # Pin for the SG90 motor

# Supabase RESTful API URL
API_URL = "https://yscyyvxduwdfjldjnwus.supabase.co"
# Supabase project API key
API_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl"
    "zY3l5dnhkdXdkZmpsZGpud3VzIiwicm9sZSI"
    "6ImFub24iLCJpYXQiOjE3MjIwNjYxMTQsImV"
    "4cCI6MjAzNzY0MjExNH0.22vV2RlrW9TU92Y"
    "79SzuOQKX8v8IISBcaHePht-43Q4"
)
# Supabase table names
TABLE_NAME = ["action_log", "sprinkler_get1", "sprinkler_get2", "sprinkler_get3"]
TODAY = dt.datetime.today()
FILE_PATH = ['data001.xlsx', 'data002.xlsx']

# Initialize each sensor
dht_sensors = {
    SENSOR_PINS[0]: adafruit_dht.DHT22(board.D17, use_pulseio=False),  # DHT22 sensor
    SENSOR_PINS[1]: adafruit_dht.DHT22(board.D27, use_pulseio=False),  # DHT11 sensor
    SENSOR_PINS[2]: adafruit_dht.DHT11(board.D22, use_pulseio=False),  # DHT11 sensor
}

# Updated motor angle dictionary (Sensor 1 -> 0 degrees, Sensor 2 -> 90 degrees, Sensor 3 -> 180 degrees)
dictionary = {1: 0, 2: 90, 3: 180}  # Mapping of sensor numbers to motor angles

servo_min_duty = 3  # Set the minimum duty cycle to 3
servo_max_duty = 12  # Set the maximum duty cycle to 12
probability = predict_probability(FILE_PATH[0], TODAY.month, TODAY.day)
pre_t, pre_h = predict_weather(FILE_PATH[1], TODAY.month, TODAY.day)

# Initialize GPIO pins
GPIO.cleanup()  # Clean up all GPIO ports
GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering mode to BCM

# Initialize each pin in SENSOR_PINS
for pin in SENSOR_PINS:
    GPIO.setup(pin, GPIO.IN)  # Set each SENSOR pin as input

GPIO.setup(PUMP, GPIO.OUT)  # Set PUMP pin as output
GPIO.setup(MOTOR, GPIO.OUT)  # Set MOTOR pin as output
servo = GPIO.PWM(MOTOR, 50)  # Set MOTOR pin to PWM mode with 50Hz frequency
servo.start(0)  # Initialize PWM with a duty cycle of 0


atexit.register(GPIO.cleanup)  # Ensure GPIO is cleaned up when the program exits

try:
    while True:
        weather_trigger, day_trigger = check_sensor_conditions()
        if weather_trigger:
            motor_angle(weather_trigger)
            GPIO.output(PUMP, GPIO.HIGH)  # Turn pump on if weather conditions are satisfied
            safe_print(f"Weather: Sensor {weather_trigger} satisfied. Pump is ON.")
            time.sleep(3)  # Keep the pump on for 3 seconds
            GPIO.output(PUMP, GPIO.LOW)  # Turn pump off

        if day_trigger:
            motor_angle(day_trigger)
            GPIO.output(PUMP, GPIO.HIGH)  # Turn pump on if day conditions are satisfied
            safe_print(f"Day: Sensor {day_trigger} satisfied. Pump is ON.")
            time.sleep(3)  # Keep the pump on for 3 seconds
            GPIO.output(PUMP, GPIO.LOW)  # Turn pump off

        else:
            safe_print("No sensor satisfied the condition. Pump remains OFF.")

        time.sleep(1)

finally:  # This block is executed when the try block exits
    servo.stop()  # Stop PWM safely
    GPIO.cleanup()  # Clean up GPIO settings
