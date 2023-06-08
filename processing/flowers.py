import numpy as np


def antispin_x(t):
    return np.cos(-t) + np.cos(3 * t)


def antispin_y(t):
    return np.sin(-t) + np.sin(3 * t)


def circle_x(t):
    return np.cos(t)


def circle_y(t):
    return np.sin(t)
