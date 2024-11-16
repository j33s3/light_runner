from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color

class RGBBox(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Inital RGB Values
        self.red = 0
        self.green = 0
        self.blue = 0
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
    def build(self):
        # Create a verticle box layout
        layout = BoxLayout(orientation='vertical', padding = 10, spacing = 10)
        self.rgb_box = RGBBox(size_hint = (1, 0.6))

        layout.add_widget(self.rgb_box)

        sliders_layout = BoxLayout(orientation = 'vertical', size_hint = (1, 0.4))

        # Red Slider
        self.red_slider = Slider(min = 0, max = 1, value = 0, step = 0.01)
        self.red_slider.bind(value = self.update_color)
        sliders_layout.add_widget(Label(text = "Red"))
        sliders_layout.add_widget(self.red_slider)

        # Green Slider
        self.green_slider = Slider(min = 0, max = 1, value = 0, step = 0.01)
        self.green_slider.bind(value = self.update_color)
        sliders_layout.add_widget(Label(text = "Green"))
        sliders_layout.add_widget(self.green_slider)

        # Blue Slider
        self.blue_slider = Slider(min = 0, max = 1, value = 0, step = 0.01)
        self.blue_slider.bind(value = self.update_color)
        sliders_layout.add_widget(Label(text = "Blue"))
        sliders_layout.add_widget(self.blue_slider)

        layout.add_widget(sliders_layout)


        return layout

    def update_color(self, instance, value):
        """Update the RGB box color when a slider value changes."""
        red = self.red_slider.value
        green = self.green_slider.value
        blue = self.blue_slider.value
        self.rgb_box.update_color(red, green, blue)


if __name__ == "__main__":
    LightInterface().run()