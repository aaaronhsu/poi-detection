import numpy as np
from file_reader import FileReader
from video_parser import VideoParser
import output

video_path: str = "processing/model/antispin.mp4"

# video = VideoParser(video_path)
# images = video.parse_video(10)  # parse at 10 frames a second

# video_data = video.detect_objects()
# video.export_coordinates("poi_short.txt")

file = FileReader("poi_short.txt")

best_parametric = file.fit_all(5)

print("Best fit:", best_parametric.type)
# output.create_graph(file.points, best_parametric.points)
output.overlay_video(video_path, best_parametric.points)
