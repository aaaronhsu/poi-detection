import numpy as np
from file_reader import FileReader
import graph
import flowers
from parametric import Parametric

file = FileReader("test.txt")

# graph.create_graph(file.points)

four_petal_antispin = Parametric(flowers.gen_antispin(0, 0, 1, 4), 250)

graph.create_graph(four_petal_antispin.points)

four_petal_antispin.dilate(5)

graph.create_graph(four_petal_antispin.points)


# realtime DO NOT USE IF FILE IS LARGE
# file.read_file_content_realtime()
