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
        dir_x_change = []
        dir_y_change = []
        dir_scale_change = []

        # TODO gradient descent on the scale of the parametric curve
        while True:
            if loss[-1] < 0.015 or (
                np.mean(dir_x_change[-6:]) == 0
                and np.mean(dir_y_change[-6:]) == 0
                and np.mean(dir_scale_change[-6:]) == 0
            ):
                break

            increase_x_loss = fitting.evaluate_transformation(
                1.01 * x_trans, y_trans, scale, cpy_poi_points, cpy_para_points
            )  # calculate the loss of the current transformation
            decrease_x_loss = fitting.evaluate_transformation(
                0.99 * x_trans, y_trans, scale, cpy_poi_points, cpy_para_points
            )  # calculate the loss of the current transformation

            delta_x_loss_increase = increase_x_loss - loss[-1]
            delta_x_loss_decrease = decrease_x_loss - loss[-1]

            increase_y_loss = fitting.evaluate_transformation(
                x_trans, 1.01 * y_trans, scale, cpy_poi_points, cpy_para_points
            )  # calculate the loss of the current transformation
            decrease_y_loss = fitting.evaluate_transformation(
                x_trans, 0.99 * y_trans, scale, cpy_poi_points, cpy_para_points
            )  # calculate the loss of the current transformation

            delta_y_loss_increase = increase_y_loss - loss[-1]
            delta_y_loss_decrease = decrease_y_loss - loss[-1]

            increase_scale_loss = fitting.evaluate_transformation(
                x_trans, y_trans, 1.01 * scale, cpy_poi_points, cpy_para_points
            )  # calculate the loss of the current transformation
            decrease_scale_loss = fitting.evaluate_transformation(
                x_trans, y_trans, 0.99 * scale, cpy_poi_points, cpy_para_points
            )  # calculate the loss of the current transformation

            delta_scale_loss_increase = increase_scale_loss - loss[-1]
            delta_scale_loss_decrease = decrease_scale_loss - loss[-1]

            if delta_x_loss_increase < delta_x_loss_decrease:
                x_trans *= 1.01
                dir_x_change.append(1)
                print("increase x loss", increase_x_loss)
            else:
                x_trans *= 0.99
                dir_x_change.append(-1)
                print("decrease x loss", decrease_x_loss)

            if delta_y_loss_increase < delta_y_loss_decrease:
                y_trans *= 1.01
                dir_y_change.append(1)
                print("increase y loss", increase_y_loss)
            else:
                y_trans *= 0.99
                dir_y_change.append(-1)
                print("decrease y loss", decrease_y_loss)

            if delta_scale_loss_increase < delta_scale_loss_decrease:
                scale *= 1.01
                dir_x_change.append(1)
                print("increase scale loss", increase_scale_loss)
            else:
                scale *= 0.99
                dir_x_change.append(-1)
                print("decrease scale loss", decrease_scale_loss)

            new_loss = fitting.evaluate_transformation(
                x_trans, y_trans, scale, cpy_poi_points, cpy_para_points
            )  # calculate the loss of the current transformation
            loss.append(new_loss)

        return loss, fitting.transform(cpy_para_points, x_trans, y_trans, scale)
