import numpy as np
from file_reader import FileReader
from video_parser import VideoParser
import graph

# video = VideoParser("processing/model/poi_short.mp4")
# images = video.parse_video(2)  # parse at 2 frames a second

# video_data = video.detect_objects()
# video.export_coordinates("poi_short.txt")

file = FileReader("poi_short.txt")

best_parametric = file.fit_all(5)

print("Best fit:", best_parametric.type)
graph.create_graph(file.points, best_parametric.points)
