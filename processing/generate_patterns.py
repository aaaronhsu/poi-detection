import random


def write_points(coords, filename):
    with open("processing/" + filename, "w+") as f:
        for point in coords:
            if random.random() < 0.8:
                continue
            f.write(
                str(5 + point[0] + random.random() / 3)
                + ","
                + str(3 + point[1] + random.random() / 3)
                + "\n"
            )
