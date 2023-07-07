import numpy as np
from point import Point


class Point:
    def __init__(self, x: float, y: float, tag: str = "") -> None:
        self.x: float = x
        self.y: float = y
        self.tag: str = tag

    def __add__(self, other: Point) -> Point:
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)

    def calculate_distance(self, point: Point) -> float:
        delta_x = self.x - point.x
        delta_y = self.y - point.y

        return np.sqrt(delta_x**2 + delta_y**2)

    def translate(self, translation: list[x:float, y:float]) -> None:
        self.x += translation[0]
        self.y += translation[1]

    def dilate(self, dilation: list[scale:float, center:Point]) -> None:
        # dilate the point by dilation
        delta_x = self.x - dilation[1].x
        delta_y = self.y - dilation[1].y

        self.x = self.x - delta_x + delta_x * dilation[0]
        self.y = self.y - delta_y + delta_y * dilation[0]
