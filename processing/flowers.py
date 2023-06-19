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


def fit_all(poi_points):
    cpy_poi_points = poi_points.copy()

    configs = []

    print("Testing 4 petal antispin...")
    four_petal_anti_loss, four_petal_anti_points = Parametric(
        gen_antispin_x(0, 1, 4), gen_antispin_y(0, 1, 4)
    ).fit(cpy_poi_points)
    configs.append(
        {
            "loss": four_petal_anti_loss,
            "points": four_petal_anti_points,
            "name": "4 petal antispin",
        }
    )
    print("Evaluated antispin loss:", four_petal_anti_loss, "\n")

    print("Testing circle...")
    circle_loss, circle_points = Parametric(gen_circle_x(0, 1), gen_circle_y(0, 1)).fit(
        cpy_poi_points
    )
    configs.append({"loss": circle_loss, "points": circle_points, "name": "Circle"})
    print("Evaluated circle loss:", circle_loss, "\n")

    # sort configs by loss
    sorted_list = sorted(configs, key=lambda x: x["loss"])

    print(
        "Best Config:",
        sorted_list[0]["name"],
        "with a loss of",
        sorted_list[0]["loss"],
    )
    return sorted_list[0]
