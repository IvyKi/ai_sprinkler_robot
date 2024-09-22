from supabase import create_client, Client
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