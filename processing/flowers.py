import numpy as np


def gen_antispin_x(trans, scale, petals, rot=0):
    return lambda t: scale * (np.cos(-t) + np.cos((petals - 1) * (t + rot))) + trans


def gen_antispin_y(trans, scale, petals, rot=0):
    return lambda t: scale * (np.sin(-t) + np.sin((petals - 1) * (t + rot))) + trans


def antispin_x(t):
    return np.cos(-t) + np.cos(3 * t)


def antispin_y(t):
    return np.sin(-t) + np.sin(3 * t)


def circle_x(t):
    return np.cos(t)


def circle_y(t):
    return np.sin(t)
