import pandas as pd
import datetime

# Load the Excel file
file_path = 'data002.xlsx'
data = pd.read_excel(file_path)

# Fill missing values in the temperature and humidity columns with their respective mean values
data['Temperature'].fillna(data['Temperature'].mean(), inplace=True)
data['Humidity'].fillna(data['Humidity'].mean(), inplace=True)

# Group the data by 'Month' and 'Day' and calculate the mean temperature and humidity for each group
average_data = data.groupby(['Month', 'Day'], as_index=False).agg({'Temperature': 'mean', 'Humidity': 'mean'})

# Define a function to return the average temperature and humidity for a given month and day
def get_avg_temp_humidity(month, day):
    result = average_data[(average_data['Month'] == month) & (average_data['Day'] == day)]
    if not result.empty:
        avg_temp = result['Temperature'].values[0]
        avg_humidity = result['Humidity'].values[0]
        return avg_temp, avg_humidity
    else:
        return None, None  # Return None if the date is not found in the data


today = datetime.date.today()
predicted_temp, predicted_humidity = get_avg_temp_humidity(int(today.month), int(today.day))

print(f"Predicted Average Temperature: {predicted_temp:.2f}°C, Predicted Average Humidity: {predicted_humidity:.2f}%")
