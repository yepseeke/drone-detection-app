from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QPushButton, QFileDialog, QFrame, QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from advanced_video_player import AdvancedVideoPlayer

background_color = (19, 19, 19)
cyan_color = (67, 252, 252)

class VideoContentWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(f"background-color: rgb{background_color};")

        self.main_layout = QVBoxLayout()
        self.advanced_video_player = AdvancedVideoPlayer()
        self.main_layout.addWidget(self.advanced_video_player, 9)

        self.buttons_layout = QHBoxLayout()

        self.upload_video_button = QPushButton()
        self.upload_video_button.setText("Загрузить видео")
        self.upload_video_button.setMinimumHeight(50)
        self.upload_video_button.setStyleSheet("QPushButton{color: rgb(67, 252, 252);border: 4px solid rgb(67, 252, 252);border-radius: 10px;font-size: 12pt;} QPushButton:hover{background-color:rgb(0,255,0); color: rgb(0, 0, 0);}")
        self.upload_video_button.clicked.connect(self.upload_video)

        self.clear_monitor_button = QPushButton()
        self.clear_monitor_button.setText("Очистить монитор")
        self.clear_monitor_button.setMinimumHeight(50)
        self.clear_monitor_button.setStyleSheet("QPushButton{color: rgb(67, 252, 252);border: 4px solid rgb(67, 252, 252);border-radius: 10px;font-size: 12pt;} QPushButton:hover{background-color:rgb(0,255,0); color: rgb(0, 0, 0);}")
        self.clear_monitor_button.clicked.connect(self.clear_video_monitor)

        self.buttons_layout.addWidget(self.upload_video_button, 1)
        self.buttons_layout.addWidget(self.clear_monitor_button, 1)
        space_widget_1 = QWidget()
        self.buttons_layout.addWidget(space_widget_1, 3)

        self.main_layout.addLayout(self.buttons_layout, 1)
        self.setLayout(self.main_layout)

    def upload_video(self):
        filepath = QFileDialog.getOpenFileName(self, "Provide path to the video", r"/",
                                               "All files (*);; MP4 Files (*.mp4)")[0]

        if len(filepath) < 3 or filepath[len(filepath) - 3: len(filepath)] != "mp4":
            raise Exception("Error: Selected file is not an video.")

        self.advanced_video_player.set_video(filepath)

    def clear_video_monitor(self):
        self.advanced_video_player.clear()


