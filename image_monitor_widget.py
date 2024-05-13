from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from video_processing import ImageProcessor

image_monitor_widget_path = r'ui/image_monitor_widget.ui'


class ImageMonitorWidget(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi(image_monitor_widget_path, self)

        self.label = self.findChild(QLabel, "label")
        self.label.setMinimumSize(1, 1)
        self.label.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: rgb(0, 0, 0);")

        self.image_processor = ImageProcessor()

        self.image_loaded = False
        self.image = None

    def set_image(self, image):
        self.image_loaded = True

        annotated_image = self.image_processor.find_objects(image)
        q_image = self.image_processor.get_QImage(annotated_image)
        image_pixmap = QPixmap.fromImage(q_image)
        scaled_image_pixmap = image_pixmap.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio)

        self.label.setPixmap(scaled_image_pixmap)

    def resizeEvent(self, event):
        if not self.image_loaded:
            return

        scaled_image = self.image.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio)
        self.label.setPixmap(scaled_image)
        QWidget.resizeEvent(self, event)

    def clear(self):
        self.image_loaded = False
        self.image = None

        self.label.clear()
