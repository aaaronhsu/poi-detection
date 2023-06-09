import math
import numpy as np
import fitting


class Parametric:
    def __init__(self, x, y, num_coordinates=250, domain=2 * math.pi):
        # takes in two functions x(t) and y(t)
        self.x = x
        self.y = y
        self.generate_coordinates(num_coordinates, domain)

    def generate_coordinates(self, num_coordinates=250, domain=2 * math.pi):
        t = np.linspace(0, domain, num_coordinates)  # store the values of t
        self.x_coords = self.x(t)  # store the values of x(t)
        self.y_coords = self.y(t)  # store the values of y(t)
        self.coords = np.stack((self.x_coords, self.y_coords), 1)
        return self.x, self.y

    def generate_loss(self, points):
        # find the minimum distance between points and the parametric curve stored in self.x_coords and self.y_coords

        loss = 0

        for point in points:
            # pass in parametric and point to find min distance
            min_dist = fitting.find_min_distance(self, point)
            loss += min_dist[1]

        # print("Loss from", points, loss)

        return loss / len(points)

    def fit(self, points):
        x_trans = 0
        y_trans = 0

        cpy_points = points.copy()
        print(points)

        current_loss = self.generate_loss(cpy_points)

        while True:
            cpy_points[:, 0] -= 0.1
            print("shifting x by 1, current loss is", current_loss)

            new_loss = self.generate_loss(cpy_points)
            print("new loss is", new_loss)

            if new_loss > current_loss:
                cpy_points[:, 0] += 0.1
                break
            current_loss = new_loss

        current_loss = new_loss

        while True:
            cpy_points[:, 1] -= 0.1
            print("shifting y by 1, current loss is", current_loss)

            new_loss = self.generate_loss(cpy_points)
            print("new loss is", new_loss)

            if new_loss > current_loss:
                cpy_points[:, 1] += 0.1
                break
            current_loss = new_loss

        return cpy_points
