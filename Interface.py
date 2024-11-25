import os

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Line, Rectangle, Color
from kivy.properties import NumericProperty
from math import atan2, degrees, sqrt

from CircularSlider import CircularSlider


class RGBBox(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Inital RGB Values
        self.red = 255
        self.green = 255
        self.blue = 255
        self.draw_color_box()

    def draw_color_box(self):
        """Draw the rectangle with the current RGB values."""
        self.canvas.clear()
        with self.canvas:
            Color(self.red, self.green, self.blue)
            Rectangle(pos=self.pos, size = self.size)
    
    def on_size(self, *args):
        """Redraw the box if the size changes."""
        self.draw_color_box()
    

    def on_pos(self, *args):
        """Redraw the box if the position changes."""
        self.draw_color_box()

    def update_color(self, red, green, blue):
        """Update the RGB values and redraw the box."""
        self.red, self.green, self.blue = red, green, blue
        self.draw_color_box()

class LightInterface(App):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller

    def build(self):
        # Load initial color and brightness
        color = self.controller.get_color()
        brightness = self.controller.get_brightness()

        # Top layout 
        topLayout = BoxLayout(orientation='vertical', padding = 10, spacing = 1)
        self.rgb_box = RGBBox(size_hint = (1, 0.1))
        topLayout.add_widget(self.rgb_box)

        # Create Body Layout
        bodyLayout = BoxLayout(orientation = 'horizontal', padding = 10, spacing = 10)

        


        # Manages the brightness slider and the on off button
        buttons_layout = BoxLayout(orientation = 'vertical', size_hint = (1, 0.75), padding = (50, 0, 0, 100))

        self.brightness_slider = Slider(min = 0, max = 1, value = brightness, step = 0.01, orientation = 'vertical', size_hint = (0.5, 1))
        self.brightness_slider.bind(value = self.update_brightness)
        buttons_layout.add_widget(self.brightness_slider)

        self.onOff_button = Button(text = 'I/O', size_hint = (0.5, 0.2))
        self.onOff_button.bind(on_press = self.onOff)
        buttons_layout.add_widget(self.onOff_button)

        bodyLayout.add_widget(buttons_layout)



        color_picker = CircularSlider(size_hint = (1.5, 1))

        color_picker.bind(knob_x = self.on_knob_position_change, knob_y = self.on_knob_position_change)

        bodyLayout.add_widget(color_picker)

        topLayout.add_widget(bodyLayout)

        return topLayout

    def on_knob_position_change(self, instance, value):
        """Callback for knob position changes."""

        os.system('clear')

        dx = instance.knob_x - instance.center_x
        dy = instance.knob_y - instance.center_y
        distance = sqrt(dx**2 + dy**2)

        if distance > instance.radius:
            # Normalize the distance
            dx *= instance.radius / distance
            dy *= instance.radius / distance
        
        angle = degrees(atan2(dy, dx)) % 360
        distance /= instance.radius
        distance = round(distance, 2)
        inverted_distance = (1 - distance) if (1 - distance) < 1 and (1 - distance) > 0 else 0
        # print(f"Angle: {angle:.2f}, Distance: {distance/instance.radius:.2f}")
        self.change_color(angle, inverted_distance)




    def update_color(self, instance, value):
        """Update the RGB box color when a slider value changes."""
        red = self.red_slider.value
        green = self.green_slider.value
        blue = self.blue_slider.value

        self.rgb_box.update_color(red, green, blue)

        if self.controller:
            self.controller.set_color((int(red * 100), int(green * 100), int(blue * 100)))

    def update_brightness(self, instance, value):
        """Updates the brightness"""
        brightness = self.brightness_slider.value

        if self.controller:
            self.controller.set_brightness(brightness)

    def onOff(self, instance):
        """Turns on and off lights"""
        if(self.controller.get_state()):
            self.controller.save_state()
            self.controller.set_state(False)
        else:
            self.controller.set_state(True)



    def change_color(self, angle, distance):
        color = [0, 0, 0]
        distance_multiplier = (distance * 100) * 2.55
        color_multiplier = ((angle - 30) % 60) * 4.25
        print(f"Distance: {distance}")
        print(f"Distance Multiplier: {distance_multiplier}")
        print(f"Color Multiplier: {color_multiplier}")


        if(angle > 30 and angle < 90):
            color[0] = 255                          # Full Red
            color[1] = 255 - color_multiplier if 255 - color_multiplier > distance_multiplier else distance_multiplier # Partial Green
            color[2] = ((distance) * 100) * 2.55
        elif(angle > 90 and angle < 150):
            color[0] = 255                          # Full Red
            color[1] = ((distance) * 100) * 2.55
            color[2] = color_multiplier if color_multiplier > distance_multiplier else distance_multiplier        # Partial Blue
        elif(angle > 150 and angle < 210):
            color[0] = 255 - color_multiplier if 255 - color_multiplier > distance_multiplier else distance_multiplier  # Partial Red
            color[1] = ((distance) * 100) * 2.55
            color[2] = 255                          # Full Blue
        elif(angle > 210 and angle < 270):
            color[0] = ((distance) * 100) * 2.55
            color[1] = color_multiplier if color_multiplier > distance_multiplier else distance_multiplier       # Partial Green
            color[2] = 255                          # Full Blue
        elif(angle > 270 and angle < 330):
            color[0] = ((distance) * 100) * 2.55
            color[1] = 255                          # Full Green
            color[2] = 255 - color_multiplier if 255 -color_multiplier > distance_multiplier else distance_multiplier # Partial Blue
        elif((angle > 330 and angle < 360) or (angle > 0 and angle < 30)):  # Looping back on angle
            color[1] = 255                          # Full green
            color[2] = ((distance) * 100) * 2.55
            if(angle > 330 and angle < 360):
                color[0] = color_multiplier if color_multiplier > distance_multiplier else distance_multiplier   # Partial Red (First half)
            else:
                color[0] = ((angle + 30) * 4.25) if ((angle + 30) * 4.25) > distance_multiplier else distance_multiplier    # Partial Red (Second Half)


        if self.controller:
            self.controller.set_color((int(color[0]), int(color[1]), int(color[2])))

        self.rgb_box.update_color(color[0], color[1], color[2])


        print(f"Color: {color[0]:.2f}, {color[1]:.2f}, {color[2]:.2f}")

        

if __name__ == "__main__":
    LightInterface().run()