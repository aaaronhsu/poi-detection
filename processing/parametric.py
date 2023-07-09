import random
from typing import Callable
from point import Point
from math import pi, sqrt
import numpy as np
import time


class Parametric:
    def __init__(
        self,
        function_data: tuple[Callable[..., float], Callable[..., float], Point],
        num_points: int = 250,
    ) -> None:
        self.center: Point = function_data[2]
        self.points: list[Point] = []
        self.type: str = function_data[3]

        # generate points with t = [0, 2pi]
        t = np.linspace(0, 2 * pi, num_points)
        for i in range(num_points):
            self.points.append(Point(function_data[0](t[i]), function_data[1](t[i])))

    def calculate_loss(self, poi_points: list[Point]) -> float:
        # calculate the loss of the fit
        poi_loss: float = 0
        for pt in poi_points:
            poi_loss += self.calculate_min_distance(pt, self.points)

        para_loss = float = 0
        for pt in self.points:
            para_loss += self.calculate_min_distance(pt, poi_points)

        return poi_loss / len(poi_points) + para_loss / len(self.points)

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

    def find_center(self, poi_points: list[Point]) -> Point:
        # find the center of the parametric curve
        center = Point(0, 0)
        for point in poi_points:
            center.x += point.x
            center.y += point.y

        center.x /= len(poi_points)
        center.y /= len(poi_points)

        return center

    def find_radius(self, poi_points: list[Point], center: Point) -> float:
        # find the radius of the parametric curve
        radius = 0
        for point in poi_points:
            radius += point.calculate_distance(center)

        return radius / len(poi_points)

    def initialize_fit(self, poi_points: list[Point]) -> None:
        # translate the parametric points to the center of the poi points
        poi_points_center: Point = self.find_center(poi_points)
        self.translate(
            (-self.center.x + poi_points_center.x, -self.center.y + poi_points_center.y)
        )

        # dilate the parametric points to the radius of the poi points
        poi_points_radius: float = self.find_radius(poi_points, poi_points_center)
        self.dilate(poi_points_radius / self.find_radius(self.points, self.center))

    def fit_points(
        self, poi_points: list[Point], timeout: int = 5
    ) -> (
        float
    ):  # fit the parametric curve to the points, with timeout default to 5 seconds
        print("Fitting points to", self.type, "for", timeout, "seconds...")
        start_time: float = time.time()

        # initialize the parametric curve to the center and radius of the poi points
        self.initialize_fit(poi_points)

        previous_loss: float = self.calculate_loss(poi_points)

        # store the best loss and points to return
        best_loss: float = previous_loss
        best_points: list[Point] = self.points
        best_center: Point = self.center
        iterations_since_best: int = 0

        # initialize gradient descent velocities
        x_velocity: float = 0
        y_velocity: float = 0
        dilation_velocity: float = 0
        discounting_factor: float = 0.2

        while time.time() - start_time < timeout:
            if iterations_since_best > 30:
                break
            # calculate the gradient of the loss function with respect to each parameter
            current_loss = previous_loss

            # set new x_velocity based on direction of gradient
            new_loss = self.calculate_translation_loss(poi_points, (0.1, 0))
            x_velocity *= discounting_factor
            x_velocity += 0.1 if new_loss < current_loss else -0.1

            # set new y_velocity based on direction of gradient
            new_loss = self.calculate_translation_loss(poi_points, (0, 0.1))
            y_velocity *= discounting_factor
            y_velocity += 0.1 if new_loss < current_loss else -0.1

            # set new dilation_velocity based on direction of gradient
            new_loss = self.calculate_dilation_loss(poi_points, 1.1)
            dilation_velocity *= discounting_factor
            dilation_velocity += 0.1 if new_loss < current_loss else -0.1

            # update the parametric curve
            self.translate((x_velocity, y_velocity))
            self.dilate(1 + dilation_velocity)

            previous_loss = self.calculate_loss(poi_points)

            if previous_loss < best_loss:
                # found a better fit
                best_loss = previous_loss
                best_points = self.points
                best_center = self.center
                iterations_since_best = 0
            iterations_since_best += 1

        # set the parametric curve to the best fit
        print("Fit complete in", round(time.time() - start_time, 2), "seconds!\n")
        self.points = best_points
        self.center = best_center

        return best_loss
