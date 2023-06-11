import math
import random
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

    def fit(self, poi_points):
        cpy_poi_points = poi_points.copy()

        x_trans, y_trans = fitting.calculate_centroid(
            cpy_poi_points
        ) - fitting.calculate_centroid(
            self.coords
        )  # calculate the translation needed to move the points to the origin
        scale = 1

        cpy_para_points = self.coords.copy()

        current_loss = fitting.evaluate_transformation(
            x_trans, y_trans, scale, cpy_poi_points, cpy_para_points
        )  # calculate the loss of the current transformation

        loss = [current_loss]

        # TODO gradient descent on the scale of the parametric curve
        while True:
            if loss[-1] < 0.1:
                break

            rng_scale = 1
            rng = random.random()
            rng_scale *= rng + 0.5
            scale_loss = fitting.evaluate_transformation(
                x_trans, y_trans, rng_scale, cpy_poi_points, cpy_para_points
            )  # calculate the loss of the current transformation
            delta_loss = scale_loss - loss[-1]  # calculate the change in loss
            if delta_loss < 0:  # if the loss decreased, keep the scale
                scale = rng_scale
            else:  # if the loss increased, revert the scale
                scale *= 1 / rng_scale
                scale_loss = fitting.evaluate_transformation(
                    x_trans, y_trans, rng_scale, cpy_poi_points, cpy_para_points
                )  # calculate the loss of the current transformation
            loss.append(scale_loss)

        return loss, fitting.transform(cpy_para_points, x_trans, y_trans, scale)
