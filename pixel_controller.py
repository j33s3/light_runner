import json
import os

import board
import neopixel

from pathlib import Path

ORDER = neopixel.GRB

BASE_PATH = Path(__file__).parent

class PixelController:

    def __init__(self, pin, num_pixels,):
        """Initializes the neopixel class wrapper"""
        self.pixels = neopixel.NeoPixel(pin, num_pixels, auto_write=False, pixel_order=ORDER)
        self.current_color = [0, 0, 0]
        self.current_state = False
    
    def set_color(self, rgb):
        """Used for setting the color"""
        self.current_color = rgb
        self.pixels.fill(rgb)
        self.pixels.show()
     
    def get_color(self):
        """Used for retrieving the color"""
        return self.current_color

    def set_brightness(self, brightness):
        """Used for changing the brightness"""
        self.pixels.brightness = brightness
        self.pixels.show()
    
    def get_brightness(self):
        """used for retrieving the brightness"""
        return self.pixels.brightness
    
    def set_state(self, power):
        """Used for managing the power state"""
        self.current_state = power

        if power is True:
            settings = self.load_state()
            print(settings)
            self.pixels.fill(settings.get("color"))
            self.pixels.brightness = settings.get("brightness")
            self.current_color = settings.get("color")
            self.pixels.show()
        else:
            self.pixels.fill((0, 0, 0))
            self.pixels.show()

    def get_state(self):
        return self.current_state

    def save_state(self):
        """Saves the state of the lights in json, saves rgb and brightness values"""
        print(f"Current Color: {self.current_color}, Current brightness: {self.pixels.brightness}")
        settings = {                                                                    # List for storing color and brightness
            "color": self.current_color,
            "brightness": self.pixels.brightness
        }

        try:
            with open(BASE_PATH / "Data" / "state.json", 'w') as file:
                json.dump(settings, file, indent=4)
            print("Settings save successfully")
        except IOError as e:
            print(f"Error writing to file: {e}")

    def load_state(self):
        """Loads the previous state from the JSON"""
        try:
            with open(BASE_PATH / "Data" / "state.json", 'r') as file:
                settings = json.load(file)                                              # parse JSON data
            print("Settings loaded successfully.")
            return settings
        except FileNotFoundError:
            print("File not found. Returning default settings")
            return {"color": [85, 85, 85], "brightness": 0.1}                           # Default Settings
        except json.JSONDecodeError:
            print("Error decoding JSON. Returning default settings")
            return {"color": [85, 85, 85], "brightness": 0.1}                           # Default Settings
        except IOError as e:
            print(f"Error reading file {e}")
            return {"color": [85, 85, 85], "brightness": 0.1}                           # Default Settings