from scipy import optimize
import numpy as np


def square_dist(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def find_min_distance(function, point):
    # find the minimum distance between the parametric (function[0], function[1]) and the points (x, y)
    # return the (values of t that minimizes the distance, the distance)
    x = point[0]
    y = point[1]

    def squared_dist(t, x, y):
        return square_dist(function[0](t), function[1](t), x, y)

    # generate array of values of t that minimize the distance
    minimum = optimize.fmin(squared_dist, 0, (x, y), disp=False)

    return minimum, squared_dist(minimum, x, y)
