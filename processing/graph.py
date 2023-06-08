import matplotlib.pyplot as plt
import numpy as np


def create_graph(coords):
    plt.scatter(coords[:, 0], coords[:, 1])
    plt.show()
