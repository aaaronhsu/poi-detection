from scipy import optimize
import numpy as np


def generate_loss(poi_points, para_points):
    # find the minimum distance between points and the parametric curve stored in self.x_coords and self.y_coords

    loss = 0

    for point in poi_points:
        # pass in parametric and point to find min distance
        min_dist = find_min_distance(point, para_points)
        loss += min_dist[1]

    # print("Loss from", points, loss)

    return loss / len(poi_points)


def evaluate_transformation(xtrans, ytrans, scale, poi_points, para_points):
    para_points = transform(
        para_points, xtrans, ytrans, scale
    )  # translate the parametric curve to the cemter of the points
    current_loss = generate_loss(poi_points, para_points)
    para_points = inv_transform(
        para_points, xtrans, ytrans, scale
    )  # translate the parametric curve back to the origin

    return current_loss


def square_dist(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def find_min_distance(point, para_points):
    x = point[0]
    y = point[1]
    min_dist = square_dist(para_points[0][0], para_points[0][1], x, y)
    min_point = para_points[0]
    for pt in para_points:
        if square_dist(pt[0], pt[1], x, y) < min_dist:
            min_dist = square_dist(pt[0], pt[1], x, y)
            min_point = pt

    return [min_point], min_dist


def calculate_centroid(points):
    # calculate the centroid of the points
    centroid = np.mean(points, axis=0)
    return centroid


def transform(points, xtrans, ytrans, scale):
    # translate the points by xtrans and ytrans, then scale by scale
    points = translate(points, xtrans, ytrans)
    points = dilate(points, scale)
    return points


def inv_transform(points, xtrans, ytrans, scale):
    # scale the points by scale, then translate by xtrans and ytrans
    points = dilate(points, 1 / scale)
    points = translate(points, -xtrans, -ytrans)
    return points


def translate(points, xtrans, ytrans):
    # translate the points by xtrans and ytrans
    points[:, 0] += xtrans
    points[:, 1] += ytrans
    return points


def dilate(points, scale):
    # scale the points by scale
    x, y = calculate_centroid(points)
    points = translate(points, -x, -y)
    points *= scale
    points = translate(points, x, y)
    return points
