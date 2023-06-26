import numpy as np
from file_reader import FileReader
import graph
import flowers

file = FileReader("test.txt")

file.read_file_content()
best_fit, previous_config = flowers.fit_all(file.coords, max_iterations=1000)
graph.create_graph_multiple([file.coords, best_fit["points"]])

# realtime DO NOT USE IF FILE IS LARGE
# file.read_file_content_realtime()
