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

    def test_fit(self, poi_points, x_trans, y_trans, scale):
        cpy_poi_points = poi_points.copy()
        cpy_para_points = self.coords.copy()

        loss = fitting.evaluate_transformation(
            x_trans, y_trans, scale, cpy_poi_points, cpy_para_points
        )

        print("the loss for ", x_trans, y_trans, scale, "is", loss)

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
        config = [x_trans, y_trans, scale]

        best_config = [x_trans, y_trans, scale]
        best_loss = current_loss

        num_iterations = 0

        # ada is learning rate
        ada = [0.1, 0.1, 0.1]

        # TODO gradient descent on the scale of the parametric curve
        while True:
            num_iterations += 1
            if num_iterations > 25:
                print("Max iterations reached")
                break

            # check if the last 10 losses are within 0.001% of each other
            last_10 = loss[-10:]
            if len(loss) > 10 and max(last_10) - min(last_10) < 0.05 * max(last_10):
                print("Converged at", num_iterations)
                break

            current_loss = loss[-1]

            gradients = []

            gradients.append(
                fitting.evaluate_transformation(
                    config[0] + random.random() * ada[0],
                    config[1],
                    config[2],
                    cpy_poi_points,
                    cpy_para_points,
                )
                - current_loss
            )  # calculate config[0] gradient
            gradients.append(
                fitting.evaluate_transformation(
                    config[0],
                    config[1] + random.random() * ada[1],
                    config[2],
                    cpy_poi_points,
                    cpy_para_points,
                )
                - current_loss
            )  # calculate config[1] gradient
            gradients.append(
                fitting.evaluate_transformation(
                    config[0],
                    config[1],
                    config[2] + random.random() * ada[2],
                    cpy_poi_points,
                    cpy_para_points,
                )
                - current_loss
            )  # calculate config[2] gradient

            # update the learning rates
            for i in range(3):
                ada[i] *= gradients[i] + 1
                config[i] -= gradients[i]

            # if num_iterations % 10 == 0:
            #     print(config[0], config[1], config[2], loss[-1])
            #     print(ada[0], ada[1], ada[2])
            #     print("\n")

            new_loss = fitting.evaluate_transformation(
                config[0], config[1], config[2], cpy_poi_points, cpy_para_points
            )  # calculate the loss of the current transformation
            loss.append(new_loss)

            if new_loss < best_loss:
                best_loss = new_loss
                best_config = config

        return (
            best_loss,
            fitting.transform(
                cpy_para_points, best_config[0], best_config[1], best_config[2]
            ),
            best_config,
        )

    def fit_nesterov(self, poi_points):
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
        config = [x_trans, y_trans, scale]

        # best_config = [x_trans, y_trans, scale, current_loss]

        num_iterations = 0

        # ada is learning rate, gamma is momentum
        ada = [0.01, 0.01, 0.01]
        gamma = [0.9, 0.9, 0.9]
        velocity = [0.1, 0.1, 0.1]

        # TODO gradient descent on the scale of the parametric curve
        while True:
            num_iterations += 1
            if num_iterations > 1000:
                print("Max iterations reached")
                print(config[0], config[1], config[2], "generates a loss of", loss[-1])

                break

            # check if the last 10 losses are within 0.001% of each other
            last_10 = loss[-10:]
            if len(loss) > 10 and max(last_10) - min(last_10) < 0.0001 * max(last_10):
                print("Converged at", num_iterations)
                print(config[0], config[1], config[2], "generates a loss of", loss[-1])
                break

            current_loss = loss[-1]

            gradients = []

            gradients.append(
                fitting.evaluate_transformation(
                    config[0] - gamma[0] * velocity[0],
                    config[1],
                    config[2],
                    cpy_poi_points,
                    cpy_para_points,
                )
                - current_loss
            )  # calculate config[0] gradient
            gradients.append(
                fitting.evaluate_transformation(
                    config[0],
                    config[1] - gamma[1] * velocity[1],
                    config[2],
                    cpy_poi_points,
                    cpy_para_points,
                )
                - current_loss
            )  # calculate config[1] gradient
            gradients.append(
                fitting.evaluate_transformation(
                    config[0],
                    config[1],
                    config[2] - gamma[2] * velocity[2],
                    cpy_poi_points,
                    cpy_para_points,
                )
                - current_loss
            )  # calculate config[2] gradient

            # update the learning rates
            for i in range(3):
                # see https://wiki.tum.de/display/lfdv/Adaptive+Learning+Rate+Method#:~:text=Adaptive%20learning%20rate%20methods%20are,the%20parameters%20of%20the%20network.
                # nesterov accelerated gradient descent
                velocity[i] = gamma[i] * velocity[i] + (ada[i] * gradients[i])
                config[i] -= velocity[i]

            print(config[0], config[1], config[2], loss[-1])

            new_loss = fitting.evaluate_transformation(
                config[0], config[1], config[2], cpy_poi_points, cpy_para_points
            )  # calculate the loss of the current transformation
            loss.append(new_loss)

        return loss, fitting.transform(cpy_para_points, config[0], config[1], config[2])
