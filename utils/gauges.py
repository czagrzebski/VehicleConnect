from kivy.uix.widget import Widget
from kivy.properties import (ListProperty, NumericProperty, ObjectProperty,
                             StringProperty)
import numpy as np
from math import cos, sin

class Gauge(Widget):
    """Partial Circular Gauge"""

    line_points = ListProperty([])
    filled_in_points = ListProperty([])

    fill_fraction = NumericProperty(.4)

    def recalculate_lines(self):

        centre_x, centre_y = self.center

        radius = self.height * 0.4

        start_angle = np.radians(220)
        end_angle = np.radians(-40)

        angles = np.linspace(start_angle, end_angle, 1000)

        line_points = []
        for angle in angles:
            line_points.append((cos(angle) * radius, sin(angle) * radius))

        self.line_points = [(x + self.center_x, y + self.center_y)
                            for x, y in line_points]

        self.filled_in_points = self.line_points[:int(
            self.fill_fraction * len(self.line_points))]


class GaugeSmall(Widget):
    """360 degree Circular Gauge"""

    line_points = ListProperty([])
    filled_in_points = ListProperty([])

    fill_fraction = NumericProperty(0)

    def recalculate_lines(self):

        centre_x, centre_y = self.center

        radius = self.height * 0.4

        start_angle = np.radians(-90)
        end_angle = np.radians(-450)

        angles = np.linspace(start_angle, end_angle, 1000)

        line_points = []
        for angle in angles:
            line_points.append((cos(angle) * radius, sin(angle) * radius))

        self.line_points = [(x + self.center_x, y + self.center_y)
                            for x, y in line_points]

        self.filled_in_points = self.line_points[:int(
            self.fill_fraction * len(self.line_points))]
