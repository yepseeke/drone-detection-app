from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QPushButton, QFileDialog
from imageMonitorWidget import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('mainWindow.ui', self)
        self.imageLayout1 = self.findChild(QHBoxLayout, "horizontalLayout_4")
        self.imageMonitorWidget = ImageMonitorWidget()
        self.imageLayout1.addWidget(self.imageMonitorWidget, 13)

        self.uploadImageButton = self.findChild(QPushButton, "uploadImageButton")
        self.uploadImageButton.clicked.connect(self.uploadImage)

        self.clearImageMonitorButton = self.findChild(QPushButton, "clearImageMonitorButton")
        self.clearImageMonitorButton.clicked.connect(self.clearImageMonitor)

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