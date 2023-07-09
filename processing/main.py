import numpy as np
from file_reader import FileReader
import graph
import flowers
from parametric import Parametric

file = FileReader("test.txt")

# graph.create_graph(file.points)

four_petal_antispin = Parametric(flowers.gen_antispin(0, 0, 1, 4), 250)

circle = Parametric(flowers.gen_circle(0, 0, 1), 250)

four_petal_antispin.fit_points(file.points)

graph.create_graph(file.points, four_petal_antispin.points)
