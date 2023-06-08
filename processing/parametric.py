import math
import numpy as np
import math_helper


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
            min_dist = math_helper.find_min_distance2(self, point)
            loss += min_dist[1]

        return loss / len(points)
