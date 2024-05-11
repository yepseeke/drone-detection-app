from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt

image_monitor_widget_path = r'ui/image_monitor_widget.ui'


class ImageMonitorWidget(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi(image_monitor_widget_path, self)

        self.label = self.findChild(QLabel, "label")
        self.label.setMinimumSize(1, 1)
        self.label.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: rgb(0, 0, 0);")

        self.image_loaded = False
        self.image = None

    def set_image(self, loaded_image):
        self.image_loaded = True

        self.image = loaded_image
        scaled_image = self.image.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio)
        self.label.setPixmap(scaled_image)

    def resize_event(self, event):
        if not self.image_loaded:
            return

        scaled_image = self.image.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio)
        self.label.setPixmap(scaled_image)
        QWidget.resizeEvent(self, event)

    def clear(self):
        self.image_loaded = False
        self.image = None

        self.label.clear()
