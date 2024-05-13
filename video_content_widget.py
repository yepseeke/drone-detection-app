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

        self.main_widget = QWidget()
        self.main_widget.setLayout(QHBoxLayout())
        self.advanced_video_player = AdvancedVideoPlayer()
        self.additional_widget = QWidget()
        self.main_widget.layout().addWidget(self.advanced_video_player, 3)
        self.main_widget.layout().addWidget(self.additional_widget, 2)
        self.additional_widget.setVisible(False)

        self.buttons_layout = QHBoxLayout()

        self.setLayout(QVBoxLayout())

        self.upload_video_button = QPushButton()
        self.upload_video_button.setText("Загрузить видео")
        self.upload_video_button.setMinimumHeight(50)
        self.upload_video_button.setStyleSheet("QPushButton{color: rgb(67, 252, 252);border: 4px solid rgb(67, 252, 252);border-radius: 10px;font-size: 12pt;} QPushButton:hover{background-color:rgb(0,255,0); color: rgb(0, 0, 0);}")
        self.upload_video_button.clicked.connect(self.upload_video)
        self.layout().addWidget(self.main_widget, 9)
        self.layout().setContentsMargins(0, 0, 9, 9)

        self.clear_monitor_button = QPushButton()
        self.clear_monitor_button.setText("Очистить монитор")
        self.clear_monitor_button.setMinimumHeight(50)
        self.clear_monitor_button.setStyleSheet("QPushButton{color: rgb(67, 252, 252);border: 4px solid rgb(67, 252, 252);border-radius: 10px;font-size: 12pt;} QPushButton:hover{background-color:rgb(0,255,0); color: rgb(0, 0, 0);}")
        self.clear_monitor_button.clicked.connect(self.clear_video_monitor)

        self.audio_monitor_button = QPushButton()
        self.audio_monitor_button.setText("Анализ звука")
        self.audio_monitor_button.setMinimumHeight(50)
        self.audio_monitor_button.setStyleSheet(
            "QPushButton{color: rgb(67, 252, 252);border: 4px solid rgb(67, 252, 252);border-radius: 10px;font-size: 12pt;} QPushButton:checked{border: 4px solid rgb(0, 255, 0);} QPushButton:hover{background-color:rgb(0,255,0); color: rgb(0, 0, 0);}")
        self.audio_monitor_button.setCheckable(True)
        self.audio_monitor_button.toggled.connect(self.additional_widget.setVisible)

        space_widget_1 = QWidget()
        self.buttons_layout.addWidget(space_widget_1, 2)
        self.buttons_layout.addWidget(self.audio_monitor_button, 1)
        self.buttons_layout.addWidget(self.clear_monitor_button, 1)
        self.buttons_layout.addWidget(self.upload_video_button, 1)

        self.layout().addLayout(self.buttons_layout, 1)

    def upload_video(self):
        filepath = QFileDialog.getOpenFileName(self, "Provide path to the video", r"/",
                                               "All files (*);; MP4 Files (*.mp4)")[0]

        if len(filepath) < 3 or filepath[len(filepath) - 3: len(filepath)] != "mp4":
            raise Exception("Error: Selected file is not an video.")

        self.advanced_video_player.set_video(filepath)

    def clear_video_monitor(self):
        self.advanced_video_player.clear()


