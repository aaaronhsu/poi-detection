import numpy as np

from point import Point
from parametric import Parametric


def calculate_loss(poi_points: list[Point], parametric: Parametric) -> float:
    # calculate the loss of the fit
    loss = 0
    for pt in poi_points:
        loss += calculate_min_distance(pt, parametric.points)

    return loss / len(poi_points)


def calculate_min_distance(point: Point, points: list[Point]) -> float:
    # calculate the minimum distance between point and list of points
    min_dist = point.distance()
    for pt in points:
        distance = point.calculate_distance(pt)
        if distance < min_dist:
            min_dist = distance

    return min_dist


def calculate_translation_loss(
    poi_points: list[Point],
    parametric: Parametric,
    translation: list[x:float, y:float],
) -> float:
    # calculate the loss of the fit after translating the parametric curve by translation
    translate_points(parametric, translation)
    loss = calculate_loss(poi_points, parametric)
    translate_points(parametric, [-translation[0], -translation[1]])

    return loss


def calculate_dilation_loss(
    poi_points: list[Point],
    parametric: Parametric,
    dilation: list[scale:float, center:Point],
) -> float:
    # calculate the loss of the fit after dilating the parametric curve by dilation
    dilate_points(parametric, dilation)
    loss = calculate_loss(poi_points, parametric)
    dilate_points(parametric, [1 / dilation[0], dilation[1]])

    return loss


def translate_points(
    parametric: Parametric, translation: list[x:float, y:float]
) -> None:
    # translate the points by translate
    for point in parametric.points:
        point.translate(translation)

    parametric.center.translate(translation)


def dilate_points(
    parametric: Parametric, dilation: list[scale:float, center:Point]
) -> None:
    # dilate the points by dilation
    for point in parametric.points:
        point.dilate(dilation)
