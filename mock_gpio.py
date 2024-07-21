# mock_gpio.py

class MockGPIO:
    BCM = "BCM"
    OUT = "OUT"
    HIGH = "HIGH"
    LOW = "LOW"

    @staticmethod
    def setmode(mode):
        print(f"Setting mode to {mode}")

    @staticmethod
    def setup(pin, mode):
        print(f"Setting up pin {pin} to mode {mode}")

    @staticmethod
    def output(pin, state):
        print(f"Setting pin {pin} to state {state}")

    @staticmethod
    def cleanup():
        print("Cleaning up GPIO")


# Alias the class to RPi.GPIO to use it transparently in your code
GPIO = MockGPIO()
