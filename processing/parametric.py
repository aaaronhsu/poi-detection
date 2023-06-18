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
        prev_gradients = [0, 0, 0]

        x_multiplier = 1
        y_multiplier = 1
        scale_multiplier = 1

        num_iterations = 0

        # TODO gradient descent on the scale of the parametric curve
        while True:
            num_iterations += 1
            if num_iterations > 1000:
                print("Max iterations reached")
                break

            # check if the last 10 losses are within 0.001% of each other
            last_10 = loss[-10:]
            if len(loss) > 10 and max(last_10) - min(last_10) < 0.0001 * max(last_10):
                print("Converged at", num_iterations)
                break

            current_loss = loss[-1]
            learning_rates = [0.001, 0.001, 0.001]

            gradients = []

            gradients.append(
                fitting.evaluate_transformation(
                    1 + x_trans, y_trans, scale, cpy_poi_points, cpy_para_points
                )
                - current_loss
            )  # calculate x_trans gradient
            gradients.append(
                fitting.evaluate_transformation(
                    x_trans, 1 + y_trans, scale, cpy_poi_points, cpy_para_points
                )
                - current_loss
            )  # calculate y_trans gradient
            gradients.append(
                fitting.evaluate_transformation(
                    x_trans, y_trans, 1 + scale, cpy_poi_points, cpy_para_points
                )
                - current_loss
            )  # calculate scale gradient

            for i in range(len(gradients)):
                if gradients[i] > prev_gradients[i]:
                    learning_rates[i] *= 1.5
                else:
                    learning_rates[i] *= 0.5

            x_trans -= learning_rates[0] * gradients[0]
            y_trans -= learning_rates[1] * gradients[1]
            scale -= learning_rates[2] * gradients[2]

            print(x_trans, y_trans, scale, loss[-1])

            new_loss = fitting.evaluate_transformation(
                x_trans, y_trans, scale, cpy_poi_points, cpy_para_points
            )  # calculate the loss of the current transformation
            loss.append(new_loss)
            prev_gradients = gradients

        return loss, fitting.transform(cpy_para_points, x_trans, y_trans, scale)
