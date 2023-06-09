import random
import numpy as np
from file_reader import FileReader
from parametric import Parametric
import graph
import flowers
import fitting

# open the file that contains the coordinates of the poi
file = FileReader("circle.txt")
coordinates = file.read_file_content()  # read and parse the file content
x_coords, y_coords = coordinates  # you can extract the coordinates like this

# # this is how you can define a parametric curve
parametric1 = Parametric(
    flowers.gen_circle_x(0, 0.5), flowers.gen_circle_y(0,0.5)
)
parametric2 = Parametric(
    flowers.gen_antispin_x(5, 1, 4), flowers.gen_antispin_y(5, 1, 4)
)

# # this is how you can plot the parametric curve
# graph.create_graph(parametric2.coords)

# # calculate how similar the two parametrics are
# loss = parametric1.generate_loss(file.coords)
# print(loss)

# # this is how you can plot the file's points
# graph.create_graph_multiple([file.coords, parametric1.coords])
# graph.create_graph_multiple([new_points, parametric1.coords])

# # same as above, but for one curve
# graph.create_graph(parametric1.coords)
# graph.create_graph(file.coords)

fitted_coords = parametric1.fit(file.coords)
graph.create_graph_multiple([file.coords, fitted_coords[1], parametric1.coords])

# print(parametric1.coords)
