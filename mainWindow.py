from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QPushButton, QFileDialog
from imageMonitorWidget import *
from video_player import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('mainWindow.ui', self)
        self.setWindowTitle("Детектор дронов")

        self.imageLayout1 = self.findChild(QHBoxLayout, "horizontalLayout_4")
        self.imageMonitorWidget = ImageMonitorWidget()
        self.imageLayout1.addWidget(self.imageMonitorWidget, 13)

        self.uploadImageButton = self.findChild(QPushButton, "uploadImageButton")
        self.uploadImageButton.clicked.connect(self.uploadImage)

        self.clearImageMonitorButton = self.findChild(QPushButton, "clearImageMonitorButton")
        self.clearImageMonitorButton.clicked.connect(self.clearImageMonitor)

        self.cameraLayout1 = self.findChild(QHBoxLayout, "horizontalLayout_2")
        self.videoPlayerWidget = VideoPlayer(0)
        self.cameraLayout1.addWidget(self.videoPlayerWidget, 13)

        self.chooseCameraButton = self.findChild(QPushButton, "chooseCameraButton")
        self.chooseCameraButton.clicked.connect(self.chooseCamera)

        self.disconnectCameraButton = self.findChild(QPushButton, "disconnectCameraButton")
        self.disconnectCameraButton.clicked.connect(self.disconnectCamera)

        self.makePhotoButton = self.findChild(QPushButton, "makePhotoButton")
        self.makePhotoButton.clicked.connect(self.makePhoto)

    def uploadImage(self):
        filepath = QFileDialog.getOpenFileName(self, "Укажите путь к картинке", "/home",
                       "All files (*);; Jpg Files (*.jpg) ;; PNG Files (*.png);")[0]
        if len(filepath) < 3 or filepath[len(filepath) - 3: len(filepath)] != "jpg" and filepath[len(filepath) - 3: len(filepath)] != "png":
            print("Not image")
            return
        pic = QPixmap(filepath)
        self.imageMonitorWidget.setImage(pic)

    def clearImageMonitor(self):
        self.imageMonitorWidget.clear()

    def chooseCamera(self):
        self.videoPlayerWidget.enable_camera()

    def disconnectCamera(self):
        self.videoPlayerWidget.disable_camera()

    def makePhoto(self):
        lastFramePixmap = self.videoPlayerWidget.lastFramePixmap
        filepath, _ = QFileDialog.getSaveFileName(self, "Укажите путь и название снимка", "", "Изображение (*.jpg)", options=QFileDialog.DontUseNativeDialog)
        lastFramePixmap.save(filepath + ".jpg")
