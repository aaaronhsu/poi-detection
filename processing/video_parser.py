import torch
from moviepy.editor import VideoFileClip
from PIL import Image


class Frame:
    def __init__(self, image: Image, number: int = -1) -> None:
        self.image = image
        self.number = number

    def show(self) -> None:
        self.image.show()

    def add_data(self, data: list) -> None:
        self.data = data
        self.parse_data()

    def parse_data(self):
        # parse the objects detected into two lists of coordinates
        self.poi_coordinates = []
        self.hand_coordinates = []

        # differntiate between poi and hand
        for data in self.data:
            if data[5] == 0:
                self.poi_coordinates.append(
                    (
                        ((data[0] + data[2]) / 2).item(),
                        ((data[1] + data[3]) / 2).item(),
                    )
                )
            elif data[5] == 1:
                self.hand_coordinates.append(
                    (
                        ((data[0] + data[2]) / 2).item(),
                        ((data[1] + data[3]) / 2).item(),
                    )
                )


class VideoParser:
    def __init__(self, video_path: str) -> None:
        self.path: str = video_path
        self.video: VideoFileClip = VideoFileClip(video_path)
        self.model = None
        self.frames: list[Frame] = []

    def load_model(self, path: str = "ALL.pt", confidence: float = 0.6) -> None:
        # loads model from .pt file
        self.model = torch.hub.load(
            "ultralytics/yolov5", "custom", path=f"processing/model/{path}"
        )
        self.model.conf = confidence

    def parse_video(self, fps: int = 10) -> list:
        # parse the video at the desired framerate and return a list of coordinates separated by frame

        self.frames = []

        for frame_num in range(0, int(self.video.duration * fps)):
            print("Parsing frame", frame_num, "of", int(self.video.duration * fps - 1))
            image = Image.fromarray(self.video.get_frame(frame_num / fps))

            self.frames.append(Frame(image, frame_num))

        return self.frames

    def detect_objects(self, frames: list[Frame] = None) -> list:
        # detects objects in the frames and adds the coordinates to the frame objects
        if self.model == None:
            print("Model not loaded. Loading default model...")
            self.load_model()

        # if no frames are inputted, detect objects in the video's saved frames
        if frames is None:
            print("No frames were inputted, detecting objects from default frames...")

            for frame in self.frames:
                print("Detecting objects in frame", f"{frame.number}...")
                frame_data = self.model(frame.image)
                frame.add_data(frame_data.xyxy[0])
        # if frames are inputted, detect objects in the inputted frames
        else:
            print("Frames were inputted, detecting objects from inputted frames...")

            for frame in frames:
                print("Detecting objects in frame", f"{frame.number}...")
                frame_data = self.model(frame.image)
                frame.add_data(frame_data.xyxy[0])
