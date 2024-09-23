import pandas as pd
import datetime


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


# Usage example
if __name__ == "__main__":
    # Initialize the Predict_weather class with the file path
    weather_processor = PredictWeather(file_path='data002.xlsx')

    # Load the data
    weather_processor.load_data()

    # Fill missing values
    weather_processor.fill_missing_values()

    # Calculate average temperature and humidity for each month and day
    weather_processor.calculate_average()

    today = datetime.datetime.today()
    # Get predicted average temperature and humidity for today's date
    predicted_temp, predicted_humidity = (weather_processor
                                          .predict_today_weather(int(today.month), int(today.day)))

    if predicted_temp is not None and predicted_humidity is not None:
        print(
            f"Predicted Average Temperature: {predicted_temp:.2f}°C, "
            f"Predicted Average Humidity: {predicted_humidity:.2f}%")
    else:
        print("No data available for today's date.")
