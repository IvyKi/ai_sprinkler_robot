# mock_adafruit.py
class DHT22:
    def __init__(self, pin):
        self.pin = pin
        self.temperature = 25.0
        self.humidity = 50.0


class DHT11(DHT22):
    pass


class MockBoard:
    D4 = 4
    D17 = 17
    D27 = 27


board = MockBoard()
