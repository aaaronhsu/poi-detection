import random
import numpy as np
from file_reader import FileReader
from parametric import Parametric
import graph
import flowers
import fitting

# open the file that contains the coordinates of the poi
file = FileReader("antispin.txt")
coordinates = file.read_file_content()  # read and parse the file content
x_coords, y_coords = coordinates  # you can extract the coordinates like this

best_fit = flowers.fit_all(file.coords)

graph.create_graph_multiple([file.coords, best_fit["points"]])
