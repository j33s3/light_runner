from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color, Line, Rectangle
from kivy.properties import NumericProperty, BooleanProperty
from math import atan2, degrees, sqrt

from kivy.core.window import Window



class CircularSlider(Widget):
    radius = NumericProperty(150) # Radius of the circular slider
    knob_size = NumericProperty(20)
    knob_pressed = BooleanProperty(False)

    knob_x = NumericProperty(0)
    knob_y = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.knob_pressed = False
        self.bind(size = self.on_size, pos = self.on_size)

        self.image_size = 460
        self.scaling_factor = 0.75

    def on_size(self, *args):
        """Ensure the widget is properly sized"""
        self.knob_x = self.center_x
        self.knob_y = self.center_y
        self.update_canvas()

    def update_canvas(self, *args):
        if not self.canvas: # Check if the canvas is initialized
            return
        self.canvas.clear()
        with self.canvas:

            scaled_size = self.image_size * self.scaling_factor
            self.circle_image = Rectangle(
                source = "colorwheel.png",
                pos = (self.center_x - scaled_size / 2, self.center_y - scaled_size / 2),
                size = (scaled_size, scaled_size),
            )




            Color(0, 0, 0, 0.4)
            Line(circle=(self.knob_x, self.knob_y, 10), width = 2.5)

            # Draw the knob
            Color(0.9, 0.9, 1, 1) # Green Color

            Line(circle=(self.knob_x, self.knob_y, 10), width = 1.5)
            # Ellipse(pos = (self.knob_x - 10, self.knob_y - 10), size = (20, 20))

    def on_touch_down(self, touch):
        """Detect when the knob is pressed"""
        if self.is_touch_on_knob(touch.pos):
            self.knob_pressed = True
            return True
        return super().on_touch_down(touch)
    
    def on_touch_up(self, touch):
        """Detect when the knob is released."""
        if self.knob_pressed:
            self.knob_pressed = False
            print("Knob released!")
            self.update_canvas()
            return True
        return super().on_touch_up(touch)

    def is_touch_on_knob(self, touch_pos):
        """Check if the touch is within the knob's bounds."""
        knob_radius = 10
        dx = touch_pos[0] - self.knob_x
        dy = touch_pos[1] - self.knob_y
        return sqrt(dx ** 2 + dy ** 2) <= knob_radius

    def on_touch_move(self, touch):
        if(self.knob_pressed):
        # if self.collide_point(*touch.pos) and self.is_inside_circle(*touch.pos):
            self.update_knob_position(*touch.pos)
            return True
        return super().on_touch_move(touch)

    def is_inside_circle(self, x, y):
        """Check if a point is within the circular area."""
        dx = x - self.center_x
        dy = y - self.center_y
        distance = sqrt(dx**2 + dy**2)
        return distance <= self.radius


    def update_knob_position(self, x, y):
        """Update the knob position within the circular boundary."""
        dx = x - self.center_x
        dy = y - self.center_y
        distance = sqrt(dx**2 + dy**2)

        if distance > self.radius: 
            # Normalize to the circle's edge
            dx *= self.radius / distance
            dy *= self.radius / distance


        self.knob_x = self.center_x + dx
        self.knob_y = self.center_y + dy

        angle = degrees(atan2(dy, dx)) % 360
        self.update_canvas()
        # print(f"Angle: {angle:.2f}, Normalized X: {dx/self.radius:.2f}, Y: {dy/self.radius:.2f}")


class CircularSliderApp(App):
    def build(self):
        slider = CircularSlider(size = (400, 400))
        return slider

if __name__ == '__main__':
    CircularSliderApp().run()