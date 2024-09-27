from supabase import create_client, Client
from trigger import Envtrigger
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


class Compare:
    """
    A class to compare temperature and humidity data from a database against predefined triggers.

    This class interacts with a Supabase database to load environmental data (such as temperature and humidity)
    and compare it with predefined threshold values. The comparison is based on the current month, and it helps
    in determining whether certain environmental conditions have been met.

    Attributes:
        day (list): A list to store the dates of the recorded data.
        time (list): A list to store the times of the recorded data.
        temp (list): A list to store the temperature values from the database.
        hum (list): A list to store the humidity values from the database.
        comp_temp (bool or None): A flag indicating whether any temperature value meets the trigger condition.
        comp_hum (bool or None): A flag indicating whether any humidity value meets the trigger condition.

    Methods:
        load_data(): Loads temperature and humidity data from the Supabase database.
        compare_temp(): Compares the loaded temperature data with predefined trigger values for the current month.
        compare_hum(): Compares the loaded humidity data with predefined trigger values for the current month.
        compare(): Compares both temperature and humidity data against their respective trigger values.
    """

    def __init__(self):
        """Initializes the Compare class with default values."""
        self.day = []
        self.time = []
        self.temp = []
        self.hum = []
        self.number = 0
        self.comp_temp = None
        self.comp_hum = None

    def select_num(self, number):
        if number:
            self.number = number
        else:
            self.number = 0

    def load_data(self):
        """Loads data from the Supabase table and populates the class attributes."""
        supabase: Client = create_client(API_URL, API_KEY)
        response = supabase.table(TABLE[self.number]).select("*").execute()
        data = response.data

        self.day = [row["day"] for row in data]
        times = [row["time"] for row in data]
        self.time = [time.split('.')[0] for time in times]
        self.temp = [row["temperature"] for row in data]
        self.hum = [row["humidity"] for row in data]

    def compare_temp(self):
        """
        Compares temperature data with the predefined trigger values for the current month.

        Loads data if not already loaded, and compares each temperature value against the
        trigger value for the current month.

        Returns:
            bool: True if any temperature value is less than or equal to the trigger value
            for the current month, False otherwise.
        """
        self.load_data()
        envtrigger = Envtrigger()

        for temp in self.temp:
            if envtrigger.temp() >= temp*100:
                self.comp_temp = True
                break
            else:
                self.comp_temp = False

        return self.comp_temp

    def compare_hum(self):
        """
        Compares humidity data with the predefined trigger values for the current month.

        Loads data if not already loaded, and compares each humidity value against the
        trigger value for the current month.

        Returns:
            bool: True if any humidity value is less than or equal to the trigger value
            for the current month, False otherwise.
        """
        self.load_data()
        envtrigger = Envtrigger()

        for hum in self.hum:
            if envtrigger.hum() >= hum*100:
                self.comp_hum = True
                break
            else:
                self.comp_hum = False

        return self.comp_hum

    def compare(self):
        """
        Compares both temperature and humidity data with predefined trigger values.

        Loads data if not already loaded, and compares both temperature and humidity values
        against the trigger values for the current month.

        Returns:
            tuple: A tuple containing two boolean values. The first represents whether any
            temperature value is less than or equal to the trigger value, and the second
            represents whether any humidity value is less than or equal to the trigger value.
        """
        self.load_data()
        self.compare_temp()
        self.compare_hum()

        return self.comp_temp, self.comp_hum


if __name__ == "__main__":
    comp = Compare()
    print(comp.compare())
