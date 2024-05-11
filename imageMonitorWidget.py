from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget, QLabel

class ImageMonitorWidget(QWidget):
    def __init__(self):
        super(ImageMonitorWidget, self).__init__()
        uic.loadUi('imageMonitorWidget.ui', self)
        self.label = self.findChild(QLabel, "label")
        self.label.setMinimumSize(1, 1)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.imageLoaded = False
        self.image = None

    def setImage(self, loadedImage):
        self.imageLoaded = True
        self.image = loadedImage
        scaledImage = self.image.scaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(scaledImage)

    def resizeEvent(self, event):
        if not self.imageLoaded:
            return
        scaledImage = self.image.scaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(scaledImage)
        QWidget.resizeEvent(self, event)

    def clear(self):
        self.imageLoaded = False
        self.image = None
        self.label.clear()