"""ai_sprinkler_robot/trigger.py

This module defines two classes
- Daytrigger: This class determines the top months and days with the highest fire frequencies,
and check if the current month and day are among the top periods.
- Envtrigger: This class provides triggers of current month's temperature data and humidity data.


. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

written by Choi Tae Hoon on 240713
-- modified by Ki Na Hye on 240720
-- featured by Choi Tae Hoon on 240730
"""
import crawler_dataportal
import crawler_fireagency
import datetime as dt
import numpy as np


class Daytrigger:
    """
    Daytrigger class to handle and analyze fire occurrence data by month and day.

    This class provides methods to load fire occurrence data, determine the top months and days
    with the highest fire frequencies, and check if the current month and day are among the top
    periods for fire occurrences.

    Attributes:
        month_list (list): A list to store fire occurrence data by month.
        day_list (list): A list to store fire occurrence data by day.
        indexed_month (list): A list to store indexed month data.
        indexed_day (list): A list to store indexed day data.
        top_month (dict): A dictionary to store the top 3 months with the highest fire frequencies.
        top_day (dict): A dictionary to store the top 5 days with the highest fire frequencies
                        for each top month.
        month_trigger (bool): A flag to indicate if the current month is one of the top months
                        for fire occurrences.
        day_trigger (bool): A flag to indicate if the current day is one of the top days
                        for fire occurrences.
    """

    def __init__(self):
        """
        Initializes an instance of the Daytrigger class.

        Initializes empty lists and dictionaries to store fire occurrence data by month and day,
        as well as the top periods for fire occurrences. Sets initial trigger flags to None.
        """
        self.month_list = []
        self.day_list = []
        self.indexed_month = []
        self.indexed_day = []
        self.top_month = {}
        self.top_day = {}
        self.month_trigger = None
        self.day_trigger = None

    def load_file(self):
        """
        Loads fire occurrence data from the data portal.

        This method calls methods from the Dataportal class
        to populate the `month_list` and `day_list` attributes.

        This method does not take any parameters or return any values.
        """
        data = crawler_dataportal.Dataportal()
        self.month_list, self.day_list = data.return_data()

    def get_top_month(self) -> dict:
        """
        Determines the top 3 months with the highest fire occurrence frequencies from the provided list.

        Returns:
            dict: A dictionary with the top 3 months and their corresponding frequencies.
              Keys are months (1 to 12) and values are frequencies.

        Notes:
            - The method stores the provided list in the instance variable `self.month_list`.
            - It generates a list of tuples where each tuple contains a month (1 to 12)
                and its corresponding frequency.
            - The list is then sorted in descending order based on frequencies.
            - The top 3 months are selected and stored in the instance variable `self.top_month`.
            - The dictionary `self.top_month` is updated with the top 3 months
                and their frequencies before being returned.

        # Example:
        #     >>> trig = Daytrigger()
        #     >>> trig.get_top_month()
        #     {3: 311, 4: 285, 2: 254}
        # """
        self.load_file()

        month_frequencies = []
        for j in range(len(self.month_list)):
            freq = self.month_list[j]
            month_frequencies.append((j+1, freq))

        # First parameter: The iterable object to be sorted (month_frequencies list).
        # key parameter: A function that provides the sorting criteria.
        # reverse -> True: Descending order.
        sorted_month_frequencies = sorted(month_frequencies, key=lambda x: x[1], reverse=True)

        temp_top_month = []
        # Extract the top 3 months with the highest frequencies
        for k in range(3):
            temp_top_month.append(sorted_month_frequencies[k])

        for index, freq in temp_top_month:
            self.top_month[index] = freq

        return self.top_month

    def get_top_day(self) -> dict:
        """
        Returns the top 5 days with the highest number of fires for each of the top 3 months.

        Returns:
            list: A list of tuples with the day and frequency of fires for the top 5 days in each of the top 3 months.


        Attributes:
            self.top_month (dict): A dictionary of the top 3 months with the highest fire occurrences.
                    Each element in the list is an object with a `key()` method
                    that returns the month as an integer (1 for January, 2 for February, etc.).
            self.top_day (dict): A dictionary where the keys are the months (from `top_month`),
                    and the values are lists of tuples representing the top 5 days
                    with the highest fire occurrences in that month.
                    Each tuple contains the day (int) and the frequency of fires (int).

        # Example:
        #     >>> data = crawler_dataportal.Dataportal()
        #     >>> trig = Daytrigger()
        #     >>> top_day_list = trig.get_top_day()
        # """
        self.load_file()

        day_frequencies = []
        for element in self.top_month:
            month_index = element.key() - 1  # Convert month (1-12) to index (0-11)
            month_data = [self.day_list[day][month_index] for day in range(31)]  # Extract data for the month

            # Create a list of (day, frequency) tuples for sorting
            day_frequencies = [(day + 1, month_data[day]) for day in range(31)]

        # Sort the days by frequency in descending order and get the top 5 days
        sorted_day_freq = sorted(day_frequencies, key=lambda x: x[1], reverse=True)[:5]

        # Append the result to top_days
        temp_day_freq = []
        for day, freq in sorted_day_freq:
            temp_day_freq.append((day, freq))

        for element in self.top_month:
            self.top_day[element] = temp_day_freq

        return self.top_day

    def check_trigger(self):
        """
        Checks if the current month and day are among the top months and days for fire occurrences.

        Raises:
            ValueError: If the current month is not in the top months list or
                        if the current day is not in the top days list for the given month.

        Returns:
            tuple: A tuple containing two boolean values:
                - `month_trigger` (bool): True if `current_month` is one of the top months
                - `day_trigger` (bool): True if `current_day` is one of the top days within the `current_month

        # Example:
        #     >>> instance = Daytrigger()
        #     >>> instance.top_month = [1, 8, 12]
        #     >>> instance.top_day = {1: [5, 10, 15], 8: [3, 8, 21], 12: [25, 30, 3]}
        #     >>> instance.check_trigger()
        #     (True, True)
        """
        today = dt.datetime.today()

        self.month_trigger = today.month in self.top_month
        if not self.month_trigger:
            self.month_trigger = False

        self.day_trigger = today.day in self.top_day.get(today.month, [])
        if not self.day_trigger:
            self.day_trigger = False

        return self.month_trigger, self.day_trigger


class Envtrigger:
    def __init__(self):
        """
        Initializes an instance of the Envtrigger class.

        Attributes:
            self.temp_list (list): A list to store temperature data.
            self.hum_list (list): A list to store humidity data.
            self.avg_temp_list (list): A list to store average temperature data.
            self.avg_hum_list (list): A list to store average humidity data.
            self.temp_trigger (float): The temperature trigger value for the current month.
            self.hum_trigger (float): The humidity trigger value for the current month.
        """
        self.temp_list = []
        self.hum_list = []
        self.avg_temp_list = []
        self.avg_hum_list = []
        self.temp_trigger = 0
        self.hum_trigger = 0
        self.temp_devi = 0.0
        self.hum_devi = 0.0

    def load_file(self):
        """
        Loads environmental data (temperature and humidity) from the fire agency.

        This method populates the following attributes:
            temp_list: List of temperature data.
            hum_list: List of humidity data.
            avg_temp_list: List of average temperature data.
            avg_hum_list: List of average humidity data.
        """
        data = crawler_fireagency.Fireagency()
        self.temp_list = data.save_temp()
        self.hum_list = data.save_hum()
        self.avg_temp_list = data.save_avg_temp()
        self.avg_hum_list = data.save_avg_hum()

    def temp(self):
        """
        Determines the temperature trigger value for the current month.

        This method sets the `temp_trigger` attribute to the average temperature of the current month.

        Returns:
            float: The temperature trigger value for the current month.
        """
        self.load_file()

        today = dt.datetime.today()
        self.temp_trigger = int(self.avg_temp_list[today.month - 1]*100)

        return self.temp_trigger

    def hum(self):
        """
        Determines the humidity trigger value for the current month.

        This method sets the `hum_trigger` attribute to the average humidity of the current month.
        """
        self.load_file()

        today = dt.datetime.today()
        self.hum_trigger = int(self.avg_hum_list[today.month-1]*100)

        return self.hum_trigger

    def hum_deviation(self):
        """
    Calculate the standard deviation of average monthly humidity.

    Returns:
        float: The standard deviation of average monthly humidity.
    [44.29, 39.67, 49.5, 39.5, 41.79, 62.95, 63.69, 69.6, 58.88, 58.91, 58.89, 52.14]
    predicted value->9.85

"""
        if not self.avg_hum_list:
            self.load_file()
        self.hum_devi = np.std(self.avg_hum_list)
        return self.hum_devi

    def temp_deviation(self):
        """
         Calculate the standard deviation of average monthly temperature.

        Returns:
                float: The standard deviation of average monthly temperature.
        [-1.61, -0.15, 8.5, 15.81, 19.97, 23.16, 28.01, 25.91, 22.22, 14.51, 10.27, -2.95]
        predicted value->10.41

        """
        if not self.avg_temp_list:
            self.load_file()
        self.temp_devi = np.std(self.avg_temp_list)
        return self.temp_devi


if __name__ == "__main__":

    example = Daytrigger()
    example2 = Envtrigger()

    hum_trigger = example2.hum()
    temp_trigger = example2.temp()
    temp_std_deviation = example2.temp_deviation()
    hum_std_deviation = example2.hum_deviation()

    print(example2.avg_temp_list)
    print(example2.avg_hum_list)

    print(temp_trigger)
    print(hum_trigger)

    print(temp_std_deviation)
    print(hum_std_deviation)
