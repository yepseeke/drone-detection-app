import cv2

from PyQt5.QtWidgets import QDialog, QHBoxLayout, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import pyqtSignal


class ChoosingCameraDialog(QDialog):
    choose_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Choose camera")
        self.layout = QHBoxLayout()
        self.choice_questions = QTreeWidget(self)
        self.choice_questions.setFixedSize(300, 200)
        self.choice_questions.setHeaderLabels(["Id", "Title", "Status"])

        self.camera_id = -1

        cameras_count_limit = 10
        for ind in range(cameras_count_limit):
            video_capture = cv2.VideoCapture(ind)
            if not video_capture.read()[0]:
                break
            item = QTreeWidgetItem([str(ind + 1), f"Device {ind + 1} is available"])
            self.choice_questions.addTopLevelItem(item)
            video_capture.release()

        self.layout.addWidget(self.choice_questions)
        self.setLayout(self.layout)
        self.choice_questions.itemDoubleClicked.connect(self.on_item_clicked)

    def on_item_clicked(self, it, col):
        self.camera_id = int(col) - 1
        self.choose_signal.emit()