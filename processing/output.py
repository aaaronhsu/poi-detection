import matplotlib.pyplot as plt
import numpy as np
from point import Point
import cv2


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
    cap = cv2.VideoCapture(video_path)

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

    try:
        frames: int = int(cap.get(cv2.cv.CAP_PROP_FRAME_COUNT))
        width: int = int(cap.get(cv2.cv.CAP_PROP_FRAME_WIDTH))
        height: int = int(cap.get(cv2.cv.CAP_PROP_FRAME_HEIGHT))
    except AttributeError:
        frames: int = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width: int = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height: int = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fig, ax = plt.subplots(1, 1)
    plt.ion()
    plt.show()

    for i in range(frames):
        point_list_num: int = 0
        fig.clf()
        flag, frame = cap.read()

        plt.imshow(frame)

        for points in point_list:
            x_coords: list[float] = []
            y_coords: list[float] = []

            for point in points:
                x_coords.append(point.x)
                y_coords.append(point.y)

            plt.scatter(x_coords, y_coords, color=colors[point_list_num % len(colors)])
            point_list_num += 1

        plt.pause(0.01)

        if cv2.waitKey(1) == 27:
            break
