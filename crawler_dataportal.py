"""ai_sprinkler_robot/crawler_dataportal.py

This module defines a class for
processing annual fire occurrence information collected
from the Data Portal Site(https://www.data.go.kr/index.do).

. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

written by Ki Na Hye on 240714
"""
import pandas as pd


class Dataportal:
    """
    A class to manage data from an Excel file containing 'Month' and 'Day' columns.

    Attributes:
        df (DataFrame): Pandas DataFrame to store the loaded data.
        col_m (Series): Pandas Series to store the 'Month' column data.
        col_d (Series): Pandas Series to store the 'Day' column data.
        month_data (list): List to store monthly counts of data.
        day_data (list): List to store daily counts per month in a pivot table format.

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

        return_data() -> 2 lists:
            Loads the file, computes monthly and monthly-daily data,
            and returns 2 lists of self.month_data(list) and self.day_data(list).
    """

    def __init__(self):
        """
        Initializes an instance of Dataportal with empty attributes.
        """
        self.df = []            # Placeholder for the DataFrame
        self.col_m = []         # Placeholder for the 'Month' column
        self.col_d = []         # Placeholder for the 'Day' column
        self.month_data = []    # Placeholder for monthly data
        self.day_data = []      # Placeholder for daily data per month

    def load_file(self):
        """
        Loads data from 'data001.xlsx' into self.df.
        Extracts 'Month' and 'Day' columns into self.col_m and self.col_d, respectively.
        """
        filename = 'data001.xlsx'
        self.df = pd.read_excel(filename)
        self.col_d = self.df['Day']
        self.col_m = self.df['Month']

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
        self.day_data = pivot_table.to_numpy().tolist()

        return self.day_data

    def return_data(self):
        """
        Loads the data, computes monthly and daily data,
        and returns lists of monthly and daily data.

        Returns:
            lists: 2 lists, each containing self.month_data and self.day_data.
        """
        self.load_file()
        self.save_month()
        self.save_month_day()

        return self.month_data, self.day_data


if __name__ == "__main__":
    # Example usage
    data = Dataportal()
    month_data, day_data = data.return_data()
    print(month_data, day_data)
