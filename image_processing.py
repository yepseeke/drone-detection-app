import cv2
import torch

from PyQt5.QtGui import QImage

from model import Model


class ImageProcessor:
    def __init__(self):
        self.model = Model()

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        if torch.cuda.is_available():
            torch.cuda.set_device(0)

        self.model.to(device=device)

    # function returns annotated frame
    def find_objects(self, image):
        result = self.model.track(image)
        annotated_image = result[0].plot()
        return annotated_image

    @staticmethod
    def get_QImage(image):
        height, width, channel = image.shape
        bytes_per_line = channel * width

        q_image = QImage(image, width, height, bytes_per_line, QImage.Format_RGB888)
        return q_image
