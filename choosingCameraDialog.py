import cv2
import sys
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class ChoosingCameraDialog(QDialog):
    chooseSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выберите камеру")
        self.layout = QHBoxLayout()
        self.cameraId = -1
        self.choice_questions = QTreeWidget(self)
        self.choice_questions.setFixedSize(300, 200)
        self.choice_questions.setHeaderLabels(["№", "Название камеры", "Статус"])
        camerasCountLimit = 10
        for ind in range(camerasCountLimit):
            video_capture = cv2.VideoCapture(ind)
            if not video_capture.read()[0]:
                break
            item = QTreeWidgetItem([str(ind + 1), "Камера " + str(ind + 1), "Активна"])
            self.choice_questions.addTopLevelItem(item)
            video_capture.release()
        self.layout.addWidget(self.choice_questions)
        self.setLayout(self.layout)
        self.choice_questions.itemDoubleClicked.connect(self.onItemClicked)

    def onItemClicked(self, it, col):
        self.cameraId = int(col) - 1
        self.chooseSignal.emit()
