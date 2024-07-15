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
    """
    A class to manage data from an Excel file
    containing 'Month', 'Day', 'Temperature' and 'Humidity' columns.

    Attributes:
        df (DataFrame): Pandas DataFrame to store the loaded data.
        col_m (Series): Pandas Series to store the 'Month' column data.
        col_d (Series): Pandas Series to store the 'Day' column data.
        col_t (Series): Pandas Series to store the 'Temperature' column data.
        col_h (Series): Pandas Series to store the 'Humidity' column data.
        month_data (list): List to store monthly counts of data.
        day_data (list): List to store daily counts per month in a pivot table format.
        temp_data (list): List to store 365 daily average temperature data.
        hum_data (list): List to store 365 daily average humidity data.
        monthly_avg_temp (list): List to store monthly average temperature.
        monthly_avg_hum (list): List to store monthly average humidity.


    Methods:
        load_file():
            Loads data from an Excel file ('data001.xlsx') into the DataFrame (self.df).
            Sets self.col_m and self.col_d based on 'Month' and 'Day' columns.

        save_month() -> list:
            Computes and saves the counts of each month's occurrences.
            Returns a list of monthly counts (self.month_data).

        save_month_day() -> list:
            Computes and saves the counts of each day per month in a pivot table format.
            Returns a list of lists (self.day_data) representing the pivot table.

        save_temp() -> list:
            Computes and saves the daily average temperatures.
            Returns a list of daily average temperatures (self.temp_data).

        save_hum() -> list:
            Computes and saves the daily average humidity.
            Returns a list of daily average humidity (self.hum_data).

        save_monthly_averages() -> tuple:
            Computes and saves the monthly average temperature and humidity.
            Returns a tuple of lists (self.monthly_avg_temp, self.monthly_avg_hum).

        return_data() -> lists:
            Loads the file, computes monthly and monthly-daily data,
            and returns 4 lists of self.month_data(list), self.day_data(list),
            self.temp_data(list), self.hum_data(list), self.monthly_avg_temp(list), and self.monthly_avg_hum(list).
    """

    def __init__(self):
        """
        Initializes an instance of Fireagency with empty attributes.
        """
        self.df = []            # Placeholder for the DataFrame
        self.col_m = []         # Placeholder for the 'Month' column
        self.col_d = []         # Placeholder for the 'Day' column
        self.col_t = []         # Placeholder for the 'Temperature' column
        self.col_h = []         # Placeholder for the 'Humidity' column
        self.month_data = []    # Placeholder for monthly data
        self.day_data = []      # Placeholder for daily data per month
        self.temp_data = []     # Placeholder for 365 daily average temperature
        self.hum_data = []      # Placeholder for 365 daily average humidity
        self.monthly_avg_temp = []  # Placeholder for monthly average temperature
        self.monthly_avg_hum = []   # Placeholder for monthly average humidity

    def load_file(self):
        """
        Loads data from 'data001.xlsx' into self.df.
        Extracts 'Month', 'Day', 'Temperature', and 'Humidity' columns into respective attributes.
        """
        filename = 'data002.xlsx'
        self.df = pd.read_excel(filename)
        self.col_d = self.df['Day']
        self.col_m = self.df['Month']
        self.col_t = self.df['Temperature']
        self.col_h = self.df['Humidity']

    def save_month(self) -> list:
        """
        Computes the count of each month's occurrences and saves it in self.month_data.

        Returns:
            list: A list of monthly counts.
        """
        month_counts = self.col_m.value_counts().reindex(range(1, 13), fill_value=0)
        self.month_data = month_counts.tolist()

        return self.month_data

    def save_month_day(self) -> list:
        """
        Computes the count of each day per month in a pivot table format and saves it in self.day_data.

        The pivot table is structured such that rows represent each
        unique day and columns represent each unique month.
        The values within the table indicate the count of occurrences.

        Returns:
            list: A list of lists representing daily counts per month.
                  Each inner list corresponds to a day and contains counts for each month,
                  filling with 0 where no data exists.
        """
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
        """
        Computes the daily average temperatures and saves it in self.temp_data.

        Returns:
            list: A list of daily average temperatures.
        """
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
        """
        Computes the daily average humidity and saves it in self.hum_data.

        Returns:
            list: A list of daily average humidity.
        """
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

    def save_monthly_averages(self) -> tuple:
        """
        Computes the monthly average temperature and humidity.

        Returns:
            tuple: A tuple containing two lists, one for monthly average temperature and one for monthly average humidity.
        """
        monthly_avg_temp = self.df.groupby('Month')['Temperature'].mean().reindex(range(1, 13), fill_value=0).tolist()
        monthly_avg_hum = self.df.groupby('Month')['Humidity'].mean().reindex(range(1, 13), fill_value=0).tolist()

        self.monthly_avg_temp = monthly_avg_temp
        self.monthly_avg_hum = monthly_avg_hum

        return self.monthly_avg_temp, self.monthly_avg_hum

    def return_data(self):
        """
        Loads the data, computes monthly and daily data,
        and returns lists of monthly and daily data.

        Returns:
            list: A list of monthly counts.
            list: A list of lists representing daily counts per month.
            list: A list of daily average temperatures.
            list: A list of daily average humidity.
            list: A list of monthly average temperatures.
            list: A list of monthly average humidity.
        """
        self.load_file()
        self.save_month()
        self.save_month_day()
        self.save_temp()
        self.save_hum()
        self.save_monthly_averages()

        return self.month_data, self.day_data, self.temp_data, self.hum_data, self.monthly_avg_temp, self.monthly_avg_hum


if __name__ == '__main__':
    data = Fireagency()
    month_data, day_data, temp_data, hum_data, monthly_avg_temp, monthly_avg_hum = data.return_data()
    print( monthly_avg_temp, monthly_avg_hum)# x=aveg_temp y=avg_hum-->return
