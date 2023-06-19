import numpy as np
from file_reader import FileReader
import graph
import flowers

# open the file that contains the coordinates of the poi
file = FileReader("antispin.txt")
coordinates = file.read_file_content()  # read and parse the file content
x_coords, y_coords = coordinates  # you can extract the coordinates like this

best_fit = flowers.fit_all(file.coords)

graph.create_graph_multiple([file.coords, best_fit["points"]])
