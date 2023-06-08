import numpy as np

# creating generic antispins does not work this way bc int + function isn't supportedt
# def gen_antispin_x(trans, scale):
#     return scale * antispin_x + trans


# def gen_antispin_y(trans, scale):
#     return scale * antispin_y + trans


def antispin_x(t):
    return np.cos(-t) + np.cos(3 * t)


def antispin_y(t):
    return np.sin(-t) + np.sin(3 * t)


def circle_x(t):
    return np.cos(t)


def circle_y(t):
    return np.sin(t)
