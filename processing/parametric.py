from typing import Callable
from point import Point
from math import pi
import numpy as np


class Parametric:
    def __init__(
        self,
        function_data: tuple[Callable[..., float], Callable[..., float], Point],
        num_points: int = 250,
    ) -> None:
        self.center: Point = function_data[2]
        self.points: list[Point] = []

        # generate points with t = [0, 2pi]
        t = np.linspace(0, 2 * pi, num_points)
        for i in range(num_points):
            self.points.append(Point(function_data[0](t[i]), function_data[1](t[i])))

    def calculate_loss(self, poi_points: list[Point]) -> float:
        # calculate the loss of the fit
        loss = 0
        for pt in poi_points:
            loss += self.calculate_min_distance(pt, self.points)

        return loss / len(poi_points)

    def calculate_min_distance(self, point: Point, points: list[Point]) -> float:
        # calculate the minimum distance between point and list of points
        min_dist = point.calculate_distance(points[0])
        for pt in points:
            distance = point.calculate_distance(pt)
            if distance < min_dist:
                min_dist = distance

        return min_dist

    def calculate_translation_loss(
        self,
        poi_points: list[Point],
        translation: tuple[float, float],
    ) -> float:
        # calculate the loss of the fit after translating the parametric curve by translation
        self.translate(translation)
        loss = self.calculate_loss(poi_points)
        self.translate((-translation[0], -translation[1]))

        return loss

    def calculate_dilation_loss(
        self,
        poi_points: list[Point],
        dilation: float,
    ) -> float:
        # calculate the loss of the fit after dilating the parametric curve by dilation
        self.dilate(dilation)
        loss = self.calculate_loss(poi_points)
        self.dilate(1 / dilation)

        return loss

    def translate(self, translation: tuple[float, float]) -> None:
        # translate the points by translate
        for point in self.points:
            point.translate(translation)

        self.center.translate(translation)

    def dilate(self, dilation: float) -> None:
        # dilate the points by dilation
        for point in self.points:
            point.dilate((dilation, self.center))

    def fit_points(
        self, poi_points: list[Point], max_iterations: int = 25
    ) -> int:  # this is the loss of the fit
        pass
