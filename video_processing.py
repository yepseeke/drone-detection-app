import cv2
import numpy as np
import torch

from ultralytics import YOLO


def to_rgb(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


class VideoProcessor:
    def __init__(self, source):
        self.video_capture = cv2.VideoCapture(source)
        self.model = YOLO(r'models/light.pt', task='detect')
        self.current_frame_index = 0

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        if torch.cuda.is_available():
            print("lol")
            torch.cuda.set_device(0)

        self.model.to(device=device)

    def get_frame(self, color_model='RGB'):
        success, frame = self.video_capture.read()
        if success:
            self.current_frame_index += 1
            if color_model == 'BGR':
                return success, np.array(frame)
            return success, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return success, frame

    # function returns annotated frame
    def find_objects(self, frame):
        result = self.model.track(frame, persist=False)
        annotated_frame = result[0].plot()
        return annotated_frame

    def get_annotated_frame(self, color_model='RGB'):
        success, frame = self.get_frame(color_model)
        if success:
            annotated_frame = self.find_objects(frame)
            return success, annotated_frame
        return success, frame

    def set_frame_index(self, frame_index: int):
        if frame_index < 0 or frame_index >= self.total_frames:
            raise Exception("Error: Frame index is out of range.")
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        self.current_frame_index = frame_index

    @property
    def total_frames(self):
        if not self.video_capture.isOpened():
            raise Exception("Error: Could not open video file.")
        return int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    @property
    def width(self):
        if not self.video_capture.isOpened():
            raise Exception("Error: Could not open video file.")
        return int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))

    @property
    def height(self):
        if not self.video_capture.isOpened():
            raise Exception("Error: Could not open video file.")
        return int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    @property
    def frame_rate(self):
        if not self.video_capture.isOpened():
            raise Exception("Error: Could not open video file.")
        return self.video_capture.get(cv2.CAP_PROP_FPS)

    def release(self):
        self.video_capture.release()
