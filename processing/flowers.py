from typing import Callable
import numpy as np
from point import Point


def gen_antispin(
    x: float, y: float, radius: float, petals: int, rot=0
) -> tuple[Callable[..., float], Callable[..., float], Point]:
    return (
        gen_antispin_x(x, radius / 2, petals, rot),
        gen_antispin_y(y, radius / 2, petals, rot),
        Point(x, y),
        "four_petal_antispin",
    )


def gen_circle(
    x: float, y: float, radius: float
) -> tuple[Callable[..., float], Callable[..., float], Point]:
    return gen_circle_x(x, radius), gen_circle_y(y, radius), Point(x, y), "circle"


def gen_antispin_x(
    trans: float, scale: float, petals: int, rot=0
) -> Callable[..., float]:
    return lambda t: scale * (np.cos(-t) + np.cos((petals - 1) * (t + rot))) + trans


def gen_antispin_y(
    trans: float, scale: float, petals: int, rot=0
) -> Callable[..., float]:
    return lambda t: scale * (np.sin(-t) + np.sin((petals - 1) * (t + rot))) + trans


def antispin_x(t: float) -> Callable[..., float]:
    return np.cos(-t) + np.cos(3 * t)


def antispin_y(t: float) -> Callable[..., float]:
    return np.sin(-t) + np.sin(3 * t)


def gen_circle_x(trans: float, scale: float) -> Callable[..., float]:
    return lambda t: scale * np.cos(t) + trans


def gen_circle_y(trans: float, scale: float) -> Callable[..., float]:
    return lambda t: scale * np.sin(t) + trans


def circle_x(t: float) -> Callable[..., float]:
    return np.cos(t)


def circle_y(t: float) -> Callable[..., float]:
    return np.sin(t)
