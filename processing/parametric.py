from point import Point
from math import pi
import numpy as np


class Parametric:
    def __init__(
        self, x_func: function, y_func: function, center: Point, num_points: int
    ) -> None:
        self.center = center
        self.points = []

        # generate points with t = [0, 2pi]
        t = np.linspace(0, 2 * pi, num_points)
        for i in range(num_points):
            self.points.append(Point(x_func(t[i]), y_func(t[i])))

    def fit_points(
        self, poi_points: list[Point], max_iterations: int = 25
    ) -> int:  # this is the loss of the fit
        pass
