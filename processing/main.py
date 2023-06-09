import random
import numpy as np
from file_reader import FileReader
from parametric import Parametric
import graph
import flowers

# open the file that contains the coordinates of the poi
file = FileReader("circle.txt")
coordinates = file.read_file_content()  # read and parse the file content
x_coords, y_coords = coordinates  # you can extract the coordinates like this

# this is how you can define a parametric curve
parametric1 = Parametric(flowers.circle_x, flowers.circle_y)
parametric2 = Parametric(
    flowers.gen_antispin_x(10, 3, 4), flowers.gen_antispin_y(10, 3, 4)
)

# this is how you can plot the parametric curve
graph.create_graph(parametric2.coords)

# calculate how similar the two parametrics are
loss = parametric1.generate_loss(file.coords)
print(loss)

new_points = parametric1.fit(file.coords)

# this is how you can plot the file's points
graph.create_graph_multiple([file.coords, parametric1.coords])
graph.create_graph_multiple([new_points, parametric1.coords])

# same as above, but for one curve
graph.create_graph(parametric1.coords)

print(parametric1.coords)
