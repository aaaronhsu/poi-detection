from point import Point
from parametric import Parametric
import flowers


class FileReader:
    def __init__(self, filename) -> None:
        self.filename: str = filename
        self.points: list[Point] = []
        self.file_content: list = []

        self.read_file_content()

    def read_file_content(self) -> list[Point]:
        with open("processing/data/" + self.filename, "r") as f:
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

    def fit_all(self, timeout: float = 5) -> Parametric:
        # fit all the parametric curves and return the best fit
        num_parametrics = 3
        time_per_parametric = round(timeout / num_parametrics, 2)

        parametrics = []

        four_petal_antispin = Parametric(flowers.gen_antispin(0, 0, 1, 4), 250)
        four_petal_antispin_loss = four_petal_antispin.fit_points(
            self.points, time_per_parametric
        )
        parametrics.append((four_petal_antispin, four_petal_antispin_loss))

        four_petal_inspin = Parametric(flowers.gen_inspin(0, 0, 1, 4), 250)
        four_petal_inspin_loss = four_petal_inspin.fit_points(
            self.points, time_per_parametric
        )
        parametrics.append((four_petal_inspin, four_petal_inspin_loss))

        circle = Parametric(flowers.gen_circle(0, 0, 1), 250)
        circle_loss = circle.fit_points(self.points, time_per_parametric)
        parametrics.append((circle, circle_loss))

        parametrics = sorted(parametrics, key=lambda x: x[1])

        return parametrics[0][0]
