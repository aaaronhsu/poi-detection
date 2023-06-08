import numpy as np
from file_reader import FileReader
from parametric import Parametric
import graph
import flowers

# open the file that contains the coordinates of the poi
file = FileReader("poi.txt")
coordinates = file.read_file_content()  # read and parse the file content
x_coords, y_coords = coordinates  # you can extract the coordinates like this

# this is how you can define a parametric curve
parametric1 = Parametric(flowers.circle_x, flowers.circle_y)
parametric2 = Parametric(flowers.antispin_x, flowers.antispin_y)

# calculate how similar the two parametrics are (note that this prints a very small number, close to 0 because it's comparing two circles)
loss = parametric1.generate_loss(parametric2.coords)
print(loss)

# this is how you can plot the file's points
graph.create_graph(file.coords)

# same as above, but for the parametric curve
graph.create_graph(parametric1.coords)
