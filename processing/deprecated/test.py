import numpy as np
import matplotlib.pyplot as plt
import time

filename = "file.txt"

with open("processing/" + filename, "r") as f:
    while True:
        line = f.readline()
        if not line or line == "\n":
            time.sleep(0.1)  # wait for 100ms before checking again
            f.seek(0, 1)  # move the file pointer to the current position
        else:
            # strip the newline character
            line = line.strip().split(",")
            if line == ["stop"]:
                break
            line = [float(x) for x in line]
            # coords = np.append(coords, [[float(line[0]), float(line[1])]], axis=0)
            print("added", line, "to coords")
            plt.scatter(line[0], line[1])
            plt.pause(1)

plt.show()
