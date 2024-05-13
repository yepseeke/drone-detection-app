from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QPushButton, QFileDialog, QFrame, QWidget

from camera_content_widget import CameraContentWidget
from image_monitor_widget import ImageMonitorWidget
from advanced_video_player import AdvancedVideoPlayer
from info_content_widget import InfoContentWidget
from settings_content_widget import SettingsContentWidget
from video_content_widget import VideoContentWidget
from video_player import VideoPlayer
from choosing_camera_dialog import ChoosingCameraDialog
from image_content_widget import ImageContentWidget

main_window_path = r'ui/main_window_styled.ui'
info_icon_path = r'images/infoIcon.svg'
menu_button_icon_path = r'images/menuIcon.svg'
camera_button_icon_path = r'images/cameraIcon.svg'
video_button_icon_path = r'images/videoIcon.svg'
image_button_icon_path = r'images/imageIcon.svg'
settings_button_icon_path = r'images/settingsIcon.svg'
info_button_icon_path = r'images/infoIcon.svg'
exit_button_icon_path = r'images/exitIcon.svg'
home_button_icon_path = r'images/homeIcon.svg'

background_color = (18, 18, 18)
title_frame_color = (15, 15, 15)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi(main_window_path, self)

        self.setWindowTitle("DroneDetectorApp")
        self.setStyleSheet(f"background-color: rgb{background_color};")

        #self.title_frame = self.findChild(QFrame, "titleFrame")
        #self.title_frame.setStyleSheet(f"background-color: rgb{title_frame_color};")

        self.expanded_menu_widget = self.findChild(QWidget, "expandedMenuWidget")
        self.expanded_menu_widget.setVisible(False)

        self.menuButton = self.findChild(QPushButton, "menuButton")
        self.menuButton.setIcon(QIcon(menu_button_icon_path))

        self.homeButton = self.findChild(QPushButton, "homeButton")
        self.homeButton.setIcon(QIcon(home_button_icon_path))
        self.homeIconButton = self.findChild(QPushButton, "homeIconButton")
        self.homeIconButton.setIcon(QIcon(home_button_icon_path))

        self.cameraButton = self.findChild(QPushButton, "cameraButton")
        self.cameraButton.setIcon(QIcon(camera_button_icon_path))
        self.cameraIconButton = self.findChild(QPushButton, "cameraIconButton")
        self.cameraIconButton.setIcon(QIcon(camera_button_icon_path))

        self.videoButton = self.findChild(QPushButton, "videoButton")
        self.videoButton.setIcon(QIcon(video_button_icon_path))
        self.videoIconButton = self.findChild(QPushButton, "videoIconButton")
        self.videoIconButton.setIcon(QIcon(video_button_icon_path))

        self.imageButton = self.findChild(QPushButton, "imageButton")
        self.imageButton.setIcon(QIcon(image_button_icon_path))
        self.imageIconButton = self.findChild(QPushButton, "imageIconButton")
        self.imageIconButton.setIcon(QIcon(image_button_icon_path))

        self.settingsButton = self.findChild(QPushButton, "settingsButton")
        self.settingsButton.setIcon(QIcon(settings_button_icon_path))
        self.settingsIconButton = self.findChild(QPushButton, "settingsIconButton")
        self.settingsIconButton.setIcon(QIcon(settings_button_icon_path))

        self.infoButton = self.findChild(QPushButton, "infoButton")
        self.infoButton.setIcon(QIcon(info_button_icon_path))
        self.infoIconButton = self.findChild(QPushButton, "infoIconButton")
        self.infoIconButton.setIcon(QIcon(info_button_icon_path))

        self.exitButton = self.findChild(QPushButton, "exitButton")
        self.exitButton.setIcon(QIcon(exit_button_icon_path))
        self.exitIconButton = self.findChild(QPushButton, "exitIconButton")
        self.exitIconButton.setIcon(QIcon(exit_button_icon_path))
        self.exitButton = self.findChild(QPushButton, "exitButton")
        self.exitButton.clicked.connect(self.close)
        self.exitIconButton.clicked.connect(self.close)

        self.contentWidget = self.findChild(QWidget, "contentWidget")

        self.imageContentWidget = ImageContentWidget()
        self.contentWidget.layout().addWidget(self.imageContentWidget, 12)
        self.imageContentWidget.setHidden(True)
        self.imageButton.toggled.connect(self.imageContentWidget.setVisible)

        self.cameraContentWidget = CameraContentWidget()
        self.contentWidget.layout().addWidget(self.cameraContentWidget, 12)
        self.cameraContentWidget.setHidden(True)
        self.cameraButton.toggled.connect(self.cameraContentWidget.setVisible)

        self.videoContentWidget = VideoContentWidget()
        self.contentWidget.layout().addWidget(self.videoContentWidget, 12)
        self.videoContentWidget.setHidden(True)
        self.videoButton.toggled.connect(self.videoContentWidget.setVisible)

        self.homeContentWidget = QWidget()
        self.contentWidget.layout().addWidget(self.homeContentWidget, 12)
        self.homeContentWidget.setHidden(True)
        self.homeButton.toggled.connect(self.homeContentWidget.setVisible)
        self.homeButton.setChecked(True)

        self.settingsContentWidget = SettingsContentWidget()
        self.contentWidget.layout().addWidget(self.settingsContentWidget, 12)
        self.settingsContentWidget.setHidden(True)
        self.settingsButton.toggled.connect(self.settingsContentWidget.setVisible)

        self.infoContentWidget = InfoContentWidget()
        self.contentWidget.layout().addWidget(self.infoContentWidget, 12)
        self.infoContentWidget.setHidden(True)
        self.infoButton.toggled.connect(self.infoContentWidget.setVisible)