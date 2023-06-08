import numpy as np


class FileReader:
    def __init__(self, filename):
        self.filename = filename

    def read_file_content(self):
        with open("yolov5/runs/tmp/poi/" + self.filename, "r") as f:
            self.file_content = f.readlines()
        return self.parse_file_content()

    def parse_file_content(self):
        self.file_content = [x.strip() for x in self.file_content]
        self.file_content = [x.split(",") for x in self.file_content]
        self.file_content = [[float(x) for x in y] for y in self.file_content]

        # shape of coordinates is (2, n)
        coordinates = np.array(self.file_content).T

        return coordinates
