import numpy as np
from file_reader import FileReader
import graph
import flowers
from parametric import Parametric

file = FileReader("test.txt")

# graph.create_graph(file.points)

# four_petal_antispin = Parametric(flowers.gen_antispin(0, 0, 1, 3), 250)

circle = Parametric(flowers.gen_circle(0, 0, 1))

graph.create_graph(circle.points)

loss = circle.calculate_loss(file.points)

loss2 = circle.calculate_translation_loss(file.points, (1, 1))

loss3 = circle.calculate_dilation_loss(file.points, 5)
print(loss)
print(loss2)
print(loss3)

graph.create_graph(circle.points, file.points)


# realtime DO NOT USE IF FILE IS LARGE
# file.read_file_content_realtime()
