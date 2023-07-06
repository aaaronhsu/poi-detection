import math
import random
import numpy as np
import fitting
import graph


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

    def fit(self, poi_points, max_iterations=25):
        cpy_poi_points = poi_points.copy()

        x_trans, y_trans = fitting.calculate_centroid(
            cpy_poi_points
        ) - fitting.calculate_centroid(
            self.coords
        )  # calculate the translation needed to move the points to the origin
        scale = 0.2

        cpy_para_points = self.coords.copy()

        current_loss = fitting.evaluate_transformation(
            x_trans, y_trans, scale, cpy_poi_points, cpy_para_points
        )  # calculate the loss of the current transformation

        loss = [current_loss]
        config = [x_trans, y_trans, scale]
        ada = [1, 1, 1]

        iterations = 0

        while iterations < max_iterations:
            iterations += 1

            if iterations % 5 == 0:
                test = fitting.transform(
                    cpy_para_points.copy(), config[0], config[1], config[1]
                )
                graph.create_graph_multiple([cpy_poi_points, test])

            for i in range(3):
                # i == (0, 1, 2) -> (x_trans, y_trans, scale)
                match i:
                    case 0:
                        x_trans_gradient = [0]
                        for modifier in range(3):
                            current_loss = loss[-1]
                            x_trans_gradient.append(
                                fitting.evaluate_transformation(
                                    config[0] + ada[0],
                                    config[1],
                                    config[2],
                                    cpy_poi_points,
                                    cpy_para_points,
                                )
                                - current_loss
                            )  # calculate config[0] gradient

                            # config[0] -= x_trans_gradient[-1]
                            # ada[0] *= (
                            #     1.1
                            #     if abs(x_trans_gradient[-1]) - abs(x_trans_gradient[-2])
                            #     > 0
                            #     else 0.9
                            # )

                            config[0] *= 1.1 if x_trans_gradient[-1] < 0 else 0.9

                            loss.append(
                                fitting.evaluate_transformation(
                                    config[0],
                                    config[1],
                                    config[2],
                                    cpy_poi_points,
                                    cpy_para_points,
                                )
                            )
                        print("x_trans_gradient", x_trans_gradient)
                    case 1:
                        y_trans_gradient = [0]
                        for iteration in range(3):
                            current_loss = loss[-1]
                            y_trans_gradient.append(
                                fitting.evaluate_transformation(
                                    config[0],
                                    config[1] + ada[1],
                                    config[2],
                                    cpy_poi_points,
                                    cpy_para_points,
                                )
                                - current_loss
                            )  # calculate config[0] gradient

                            # config[1] -= y_trans_gradient[-1]
                            # ada[1] *= (
                            #     1.1
                            #     if abs(y_trans_gradient[-1]) - abs(y_trans_gradient[-2])
                            #     > 0
                            #     else 0.9
                            # )

                            config[1] *= 1.1 if y_trans_gradient[-1] < 0 else 0.9

                            loss.append(
                                fitting.evaluate_transformation(
                                    config[0],
                                    config[1],
                                    config[2],
                                    cpy_poi_points,
                                    cpy_para_points,
                                )
                            )
                        print("y_trans_gradient", y_trans_gradient)
                    case 2:
                        scale_gradient = [0]
                        for iteration in range(3):
                            current_loss = loss[-1]
                            scale_gradient.append(
                                fitting.evaluate_transformation(
                                    config[0],
                                    config[1],
                                    config[2] + ada[2],
                                    cpy_poi_points,
                                    cpy_para_points,
                                )
                                - current_loss
                            )  # calculate config[0] gradient

                            print(
                                "increasing scale by",
                                ada[2],
                                "yields a loss of",
                                scale_gradient[-1],
                            )

                            # config[2] -= scale_gradient[-1]
                            # config[2] = max(config[2], 0.1)
                            # ada[2] *= (
                            #     1.1
                            #     if abs(scale_gradient[-1]) - abs(scale_gradient[-2]) > 0
                            #     else 0.9
                            # )

                            config[2] *= 0.9 if scale_gradient[-1] < 0 else 1.1

                            loss.append(
                                fitting.evaluate_transformation(
                                    config[0],
                                    config[1],
                                    config[2],
                                    cpy_poi_points,
                                    cpy_para_points,
                                )
                            )

                        print("scale_gradient", scale_gradient)

        return (
            loss[-1],
            fitting.transform(cpy_para_points, config[0], config[1], config[2]),
            config,
        )

    def old_fit(self, poi_points, max_iterations=25):
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
            if num_iterations > max_iterations:
                print("Max iterations reached")
                break

            # check if the last 10 losses are within 0.001% of each other
            last_10 = loss[-10:]
            if len(loss) > 10 and max(last_10) - min(last_10) < 0.05 * max(last_10):
                print("Converged at", num_iterations)
                break

            current_loss = loss[-1]

            gradients = []
            step_size = [random.random(), random.random(), random.random()]

            gradients.append(
                fitting.evaluate_transformation(
                    config[0] + step_size[0] * ada[0],
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
                    config[1] + step_size[1] * ada[1],
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
                    config[2] + step_size[2] * ada[2],
                    cpy_poi_points,
                    cpy_para_points,
                )
                - current_loss
            )  # calculate config[2] gradient

            # update the learning rates
            for i in range(2):
                # ada[i] *= gradients[i] + 1
                config[i] -= gradients[i] * step_size[i]

            print(gradients)

            # if num_iterations % 10 == 0:
            #     print(config[0], config[1], config[2], loss[-1])
            #     print(ada[0], ada[1], ada[2])
            #     print("\n")

            testing = fitting.transform(
                cpy_para_points, config[0], config[1], config[2]
            )
            graph.create_graph_multiple([cpy_poi_points, testing])

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
