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
# parametric2 = Parametric(flowers.antispin_x, flowers.antispin_y)


# # calculate how similar the two parametrics are (note that this prints a very small number, close to 0 because it's comparing two circles)
loss = parametric1.generate_loss(file.coords)

# print(file.coords, parametric1.coords)
# print(loss)

new_points = parametric1.fit(file.coords)
# print(new_points)

# # this is how you can plot the file's points
graph.create_graph_multiple([file.coords, parametric1.coords])
graph.create_graph_multiple([new_points, parametric1.coords])

# # same as above, but for the parametric curve
# graph.create_graph(parametric1.coords)

# print(parametric1.coords)


# with open("processing/circle.txt", "w+") as f:
#     for point in parametric1.coords:
#         if random.random() < 0.8:
#             continue
#         f.write(
#             str(5 + point[0] + random.random() / 3)
#             + ","
#             + str(3 + point[1] + random.random() / 3)
#             + "\n"
#         )
