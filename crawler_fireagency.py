"""ai_sprinkler_robot/crawler_fireagency.py

This module defines a class for
processing annual fire occurrence information and temperature, humidity data
collected from the National Fire Agency(https://www.nfa.go.kr/nfa/).

. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

written by Choi Tae Hoon on 240713
-- modified by Ki Na Hye on 240714
"""
import pandas as pd


class Fireagency:
    def __init__(self):

        self.monthly_avg_hum = None
        self.monthly_avg_temp = None
        self.df = []            # Placeholder for the DataFrame
        self.col_m = []         # Placeholder for the 'Month' column
        self.col_d = []         # Placeholder for the 'Day' column
        self.col_t = []         # Placeholder for the 'Temperature' column
        self.col_h = []         # Placeholder for the 'Humidity' column
        self.month_data = []    # Placeholder for monthly data
        self.day_data = []      # Placeholder for daily data per month
        self.temp_data = []     # Placeholder for 365 daily average temperature
        self.hum_data = []      # Placeholder for 365 daily average humidity

    def load_file(self):

        filename = 'data002.xlsx'
        self.df = pd.read_excel(filename)
        self.col_d = self.df['Day']
        self.col_m = self.df['Month']
        self.col_t = self.df['Temperature']
        self.col_h = self.df['Humidity']

    def save_month(self) -> list:

        self.load_file()

        df1 = pd.DataFrame({
            'month': self.col_m,
            'day': self.col_d
        })

        month_counts = df1['month'].value_counts().reindex(range(1, 13), fill_value=0)
        self.month_data = month_counts.tolist()

        return self.month_data

    def save_month_day(self) -> list:

        df1 = pd.DataFrame({
            'month': self.col_m,
            'day': self.col_d
        })

        day_counts = df1.groupby(['month', 'day']).size().reset_index(name='count')
        pivot_table = day_counts.pivot(index='day', columns='month', values='count').fillna(0)

        # Extracting the daily counts per month values into lists
        self.day_data = pivot_table.to_numpy().tolist()

        return self.day_data

    def save_temp(self) -> list:

        df1 = pd.DataFrame({
            'Month': self.col_m,
            'Day': self.col_d,
            'Temperature': self.col_t,
        })

        daily_averages = (df1.groupby(['Month', 'Day'])
                          .agg({'Temperature': 'mean'}).reset_index())

        # Extracting the average temperature values into a list
        self.temp_data = daily_averages['Temperature'].tolist()

        return self.temp_data

    def save_hum(self) -> list:

        df1 = pd.DataFrame({
            'Month': self.col_m,
            'Day': self.col_d,
            'Humidity': self.col_h
        })

        daily_averages = (df1.groupby(['Month', 'Day'])
                          .agg({'Humidity': 'mean'}).reset_index())

        # Extracting the average humidity values into a list
        self.hum_data = daily_averages['Humidity'].tolist()

        return self.hum_data

    def save_avg_temp(self):

        self.load_file()

        df1 = pd.DataFrame({
            'Month': self.col_m,
            'Day': self.col_d,
            'Temperature': self.col_t,
        })

        monthly_avg_temp = (df1.groupby('Month')['Temperature']
                            .mean()
                            .reindex(range(1, 13), fill_value=0)
                            .apply(lambda x: round(x, 2))
                            .tolist())

        self.monthly_avg_temp = monthly_avg_temp

        return self.monthly_avg_temp

    def save_avg_hum(self):

        self.load_file()

        df1 = pd.DataFrame({
            'Month': self.col_m,
            'Day': self.col_d,
            'Humidity': self.col_h
        })

        monthly_avg_hum = (df1.groupby('Month')['Humidity']
                           .mean()
                           .reindex(range(1, 13), fill_value=0)
                           .apply(lambda x: round(x, 2))
                           .tolist())

        self.monthly_avg_hum = monthly_avg_hum

        return self.monthly_avg_hum

    def return_data(self):

        self.load_file()
        self.save_month()
        self.save_month_day()
        self.save_temp()
        self.save_hum()

        return self.month_data, self.day_data, self.temp_data, self.hum_data


if __name__ == '__main__':
    data = Fireagency()
    data.load_file()
    average_temp = data.save_avg_temp()
    average_hum = data.save_avg_hum()
    print(average_temp)
    print(average_hum)
