from point import Point


class FileReader:
    def __init__(self, filename) -> None:
        self.filename: str = filename
        self.points: list[Point] = []
        self.file_content: list = []

        self.read_file_content()

    def read_file_content(self) -> list[Point]:
        with open("processing/" + self.filename, "r") as f:
            self.file_content = f.readlines()
        return self.parse_file_content()

    def parse_file_content(self) -> list[Point]:
        self.file_content = [x.strip() for x in self.file_content]
        self.file_content = [x.split(",") for x in self.file_content]
        self.file_content = [[float(x) for x in y] for y in self.file_content]

        # shape of coords is (n, 2)
        for x, y in self.file_content:
            self.points.append(Point(x, y))

        return self.points
