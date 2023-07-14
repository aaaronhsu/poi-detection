import matplotlib.pyplot as plt
import numpy as np
from point import Point


def create_graph(*point_list: list[Point]) -> None:
    colors: list[str] = [
        "red",
        "blue",
        "green",
        "purple",
        "orange",
        "yellow",
        "pink",
        "black",
    ]

    point_list_num: int = 0

    for points in point_list:
        x_coords: list[float] = []
        y_coords: list[float] = []

        for point in points:
            x_coords.append(point.x)
            y_coords.append(point.y)

        plt.scatter(x_coords, y_coords, color=colors[point_list_num % len(colors)])
        point_list_num += 1

    plt.show()


def overlay_video(video_path: str, *point_list: list[Point]) -> None:
    # overlay the video with the parametric curve
    pass
