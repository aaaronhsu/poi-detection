import numpy as np
from file_reader import FileReader
import graph

file = FileReader("test.txt")

best_parametric = file.fit_all(1)

print("Best fit:", best_parametric.type)
graph.create_graph(file.points, best_parametric.points)
