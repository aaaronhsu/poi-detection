import numpy as np
from parametric import Parametric


def gen_antispin_x(trans, scale, petals, rot=0):
    return lambda t: scale * (np.cos(-t) + np.cos((petals - 1) * (t + rot))) + trans


def gen_antispin_y(trans, scale, petals, rot=0):
    return lambda t: scale * (np.sin(-t) + np.sin((petals - 1) * (t + rot))) + trans


def antispin_x(t):
    return np.cos(-t) + np.cos(3 * t)


def antispin_y(t):
    return np.sin(-t) + np.sin(3 * t)


def gen_circle_x(trans, scale):
    return lambda t: scale * np.cos(t) + trans


def gen_circle_y(trans, scale):
    return lambda t: scale * np.sin(t) + trans


def circle_x(t):
    return np.cos(t)


def circle_y(t):
    return np.sin(t)


def fit_three_petal_antispin(poi_points, prior=[0, 0, 1]):
    print("Testing 3 petal antispin...")

    parametric = None

    parametric = Parametric(
        gen_antispin_x(prior[0], prior[2], 3),
        gen_antispin_y(prior[1], prior[2], 3),
    )

    three_petal_anti_loss, three_petal_anti_points, best_config = parametric.fit(
        poi_points
    )

    print("Evaluated three petal antispin loss:", three_petal_anti_loss)
    print("Config for three petal antispin:", best_config, "\n")

    return {
        "loss": three_petal_anti_loss,
        "points": three_petal_anti_points,
        "name": "3 petal antispin",
        "config": best_config,
    }


def fit_four_petal_antispin(poi_points, prior=[0, 0, 1]):
    print("Testing 4 petal antispin...")

    parametric = None

    parametric = Parametric(
        gen_antispin_x(prior[0], prior[2], 4),
        gen_antispin_y(prior[1], prior[2], 4),
    )

    four_petal_anti_loss, four_petal_anti_points, best_config = parametric.fit(
        poi_points
    )

    print("Evaluated four petal antispin loss:", four_petal_anti_loss)
    print("Config for four petal antispin:", best_config, "\n")

    return {
        "loss": four_petal_anti_loss,
        "points": four_petal_anti_points,
        "name": "4 petal antispin",
        "config": best_config,
    }


def fit_circle(poi_points, prior=[0, 0, 1]):
    print("Testing circle...")

    parametric = None

    parametric = Parametric(
        gen_circle_x(prior[0], prior[2]),
        gen_circle_y(prior[1], prior[2]),
    )

    circle_loss, circle_points, best_config = parametric.fit(poi_points)

    print("Evaluated circle loss:", circle_loss)
    print("Config for circle:", best_config, "\n")

    return {
        "loss": circle_loss,
        "points": circle_points,
        "name": "circle",
        "config": best_config,
    }


def fit_all(poi_points, prior=[[0, 0, 1], [0, 0, 1], [0, 0, 1]]):
    print("Fitting all flowers...\n")
    configs = []

    three_petal_antispin = fit_three_petal_antispin(poi_points, prior[0])
    configs.append(three_petal_antispin)

    four_petal_antispin = fit_four_petal_antispin(poi_points, prior[1])
    configs.append(four_petal_antispin)

    circle = fit_circle(poi_points, prior[2])
    configs.append(circle)

    # sort configs by loss
    sorted_list = sorted(configs, key=lambda x: x["loss"])

    print(
        "Best Config:",
        sorted_list[0]["name"],
        "with a loss of",
        sorted_list[0]["loss"],
    )
    return sorted_list[0], [
        three_petal_antispin["config"],
        four_petal_antispin["config"],
        circle["config"],
    ]
