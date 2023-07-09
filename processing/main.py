import numpy as np
from file_reader import FileReader
import graph
import flowers
from parametric import Parametric

file = FileReader("test.txt")

best_parametric = file.fit_all()

print("Best fit:", best_parametric.type)
graph.create_graph(file.points, best_parametric.points)
