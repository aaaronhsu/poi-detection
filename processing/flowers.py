import numpy as np
from point import Point


def gen_antispin(x: float, y: float, radius: float, petals: int, rot=0) -> function:
    return [
        gen_antispin_x(x, radius, petals, rot),
        gen_antispin_y(y, radius, petals, rot),
        Point(x, y),
    ]


def gen_circle(x: float, y: float, radius: float) -> function:
    return [
        gen_circle_x(x, radius),
        gen_circle_y(y, radius),
        Point(x, y),
    ]


def gen_antispin_x(trans: float, scale: float, petals: int, rot=0) -> function:
    return lambda t: scale * (np.cos(-t) + np.cos((petals - 1) * (t + rot))) + trans


def gen_antispin_y(trans: float, scale: float, petals: int, rot=0) -> function:
    return lambda t: scale * (np.sin(-t) + np.sin((petals - 1) * (t + rot))) + trans


def antispin_x(t: float) -> function:
    return np.cos(-t) + np.cos(3 * t)


def antispin_y(t: float) -> function:
    return np.sin(-t) + np.sin(3 * t)


def gen_circle_x(trans: float, scale: float) -> function:
    return lambda t: scale * np.cos(t) + trans


def gen_circle_y(trans: float, scale: float) -> function:
    return lambda t: scale * np.sin(t) + trans


def circle_x(t: float) -> function:
    return np.cos(t)


def circle_y(t: float) -> function:
    return np.sin(t)
