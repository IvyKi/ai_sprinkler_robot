"""ai_sprinkler_robot/crawler_dataportal.py

This module defines a class for
processing annual fire occurrence information
collected from the Data Portal Site(https://www.data.go.kr/index.do).

. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

written by Ki Na Hye on 240714
"""
import pandas as pd


class Dataportal:
    def __init__(self):

        self.df = []            # Placeholder for the DataFrame
        self.col_m = []         # Placeholder for the 'Month' column
        self.col_d = []         # Placeholder for the 'Day' column
        self.month_data = []    # Placeholder for monthly data
        self.day_data = []      # Placeholder for daily data per month

    def load_file(self):

        filename = 'data001.xlsx'
        self.df = pd.read_excel(filename)
        self.col_d = self.df['Day']
        self.col_m = self.df['Month']

    def save_month(self) -> list:

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
        self.day_data = pivot_table.to_numpy().tolist()

        return self.day_data

    def return_data(self):

        self.load_file()
        self.save_month()
        self.save_month_day()

        return self.month_data, self.day_data


if __name__ == "__main__":
    # Example usage
    data = Dataportal()
    month_data, day_data = data.return_data()
    print(month_data)
    print(type(month_data))
