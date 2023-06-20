import numpy as np
import time


class FileReader:
    def __init__(self, filename):
        self.filename = filename
        self.coords = np.empty((0, 2))

    def read_file_content_realtime(self):
        with open("processing/" + self.filename, "r") as f:
            while True:
                line = f.readline()
                if not line or line == "\n":
                    time.sleep(0.1)  # wait for 100ms before checking again
                    f.seek(0, 1)  # move the file pointer to the current position
                else:
                    # strip the newline character
                    line = line.strip().split(",")
                    line = [float(x) for x in line]
                    self.coords = np.append(
                        self.coords, [[float(line[0]), float(line[1])]], axis=0
                    )
                    print("added", line, "to coords")

    def read_file_content(self):
        with open("processing/" + self.filename, "r") as f:
            self.file_content = f.readlines()
        return self.parse_file_content()

    def parse_file_content(self):
        self.file_content = [x.strip() for x in self.file_content]
        self.file_content = [x.split(",") for x in self.file_content]
        self.file_content = [[float(x) for x in y] for y in self.file_content]

        # shape of coords is (n, 2)
        self.coords = np.array(self.file_content)

        # but we return the transpose so we can easily access the x and y coordinates
        return self.coords.T
