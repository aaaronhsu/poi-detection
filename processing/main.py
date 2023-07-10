import numpy as np
from file_reader import FileReader
from video_parser import VideoParser
import graph

video = VideoParser("processing/model/poi_short.mp4")
images = video.parse_video(2)  # parse at 2 frames a second

video_data = video.detect_objects()

for frame in video.frames:
    print(
        "frame",
        frame.number,
        "poi:",
        frame.poi_coordinates,
        "hand:",
        frame.hand_coordinates,
    )

# poi_coordinates, hand_coordinates = video.extract_object_coordinates()

# print(poi_coordinates)
# print(hand_coordinates)

# file = FileReader("test.txt")

# best_parametric = file.fit_all(1)

# print("Best fit:", best_parametric.type)
# graph.create_graph(file.points, best_parametric.points)
