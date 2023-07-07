import matplotlib.pyplot as plt
import numpy as np


def create_graph(coords):
    plt.scatter(coords[:, 0], coords[:, 1])
    plt.show()


def create_graph_multiple(coords):
    colors = ["red", "blue", "green", "purple", "orange", "yellow", "pink", "black"]

    for i in range(len(coords)):
        plt.scatter(coords[i][:, 0], coords[i][:, 1], color=colors[i])
    plt.show()
