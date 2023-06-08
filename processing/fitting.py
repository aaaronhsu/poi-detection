from scipy import optimize
import numpy as np


def square_dist(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def find_min_distance(parametric, point):
    x = point[0]
    y = point[1]
    min_dist = square_dist(parametric.coords[0][0], parametric.coords[0][1], x, y)
    min_point = parametric.coords[0]
    for pt in parametric.coords:
        if square_dist(pt[0], pt[1], x, y) < min_dist:
            min_dist = square_dist(pt[0], pt[1], x, y)
            min_point = pt

    return [pt], min_dist


# this function is the same as the function above, but uses optimize.fmin which is less accurate
def find_min_distance_opt(parametric, point):
    # find the minimum distance between the parametric (function[0], function[1]) and the points (x, y)
    # return the (values of t that minimizes the distance, the distance)
    x = point[0]
    y = point[1]

    def squared_dist(t, x, y):
        return square_dist(parametric.x(t), parametric.y(t), x, y)

    # generate array of values of t that minimize the distance
    minimum = optimize.fmin(squared_dist, 0, (x, y), disp=False)

    return minimum, squared_dist(minimum, x, y)
