from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QPushButton, QFileDialog, QFrame

from image_monitor_widget import ImageMonitorWidget
from advanced_video_player import AdvancedVideoPlayer
from video_player import VideoPlayer
from choosing_camera_dialog import ChoosingCameraDialog

main_window_path = r'ui/main_window.ui'
info_icon_path = r'images/infoIcon.svg'

background_color = (18, 18, 18)
title_frame_color = (15, 15, 15)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi(main_window_path, self)

        self.setWindowTitle("DroneDetectorApp")
        self.setStyleSheet(f"background-color: rgb{background_color};")

        self.title_frame = self.findChild(QFrame, "titleFrame")
        self.title_frame.setStyleSheet(f"background-color: rgb{title_frame_color};")

        self.info_button = self.findChild(QPushButton, "infoButton")
        self.info_button.clicked.connect(self.show_info)

        self.image_layout_1 = self.findChild(QHBoxLayout, "horizontalLayout_4")
        self.image_monitor_widget = ImageMonitorWidget()
        self.image_layout_1.addWidget(self.image_monitor_widget, 13)

        self.upload_image_button = self.findChild(QPushButton, "uploadImageButton")
        self.upload_image_button.clicked.connect(self.upload_image)

        self.clear_image_monitor_button = self.findChild(QPushButton, "clearImageMonitorButton")
        self.clear_image_monitor_button.clicked.connect(self.clear_image_monitor)

        self.camera_layout_1 = self.findChild(QHBoxLayout, "horizontalLayout_2")
        self.video_player_widget = VideoPlayer()
        self.camera_layout_1.addWidget(self.video_player_widget, 13)

        self.choose_camera_button = self.findChild(QPushButton, "chooseCameraButton")
        self.choose_camera_button.clicked.connect(self.choose_camera)

        self.disconnect_camera_button = self.findChild(QPushButton, "disconnectCameraButton")
        self.disconnect_camera_button.clicked.connect(self.disconnect_camera)

        self.make_photo_button = self.findChild(QPushButton, "makePhotoButton")
        self.make_photo_button.clicked.connect(self.make_photo)

        self.info_button = self.findChild(QPushButton, "infoButton")
        self.info_button.setIcon(QIcon(info_icon_path))

        self.video_layout_1 = self.findChild(QHBoxLayout, "horizontalLayout_3")
        self.advanced_video_player_widget = AdvancedVideoPlayer()
        self.video_layout_1.addWidget(self.advanced_video_player_widget, 13)

        self.upload_video_button = self.findChild(QPushButton, "uploadVideoButton")
        self.upload_video_button.clicked.connect(self.upload_video)

        self.clear_video_monitor_button = self.findChild(QPushButton, "clearVideoMonitorButton")
        self.clear_video_monitor_button.clicked.connect(self.clear_video_monitor)

        self.choosing_camera_dialog = None

    def show_info(self):
        pass

    def upload_image(self):
        filepath = QFileDialog.getOpenFileName(self, "Provide path to the image", r"/",
                                               "All files (*);; Jpg Files (*.jpg) ;; PNG Files (*.png);")[0]

        if len(filepath) < 3 or filepath[len(filepath) - 3: len(filepath)] != "jpg" and filepath[len(filepath) - 3: len(
                filepath)] != "png":
            raise Exception("Error: Selected file is not an image.")

        image = QPixmap(filepath)
        self.image_monitor_widget.set_image(image)

    def upload_video(self):
        filepath = QFileDialog.getOpenFileName(self, "Provide path to the video", r"/",
                                               "All files (*);; MP4 Files (*.mp4)")[0]

        if len(filepath) < 3 or filepath[len(filepath) - 3: len(filepath)] != "mp4":
            raise Exception("Error: Selected file is not an video.")

        self.advanced_video_player_widget.set_video(filepath)

    def clear_image_monitor(self):
        self.image_monitor_widget.clear()

    def clear_video_monitor(self):
        self.advanced_video_player_widget.clear()

    def choose_camera(self):
        self.choosing_camera_dialog = ChoosingCameraDialog()
        self.choosing_camera_dialog.choose_signal.connect(self.turn_on_camera)
        self.choosing_camera_dialog.show()
        self.choosing_camera_dialog.exec_()

    def turn_on_camera(self):
        camera_id = self.choosing_camera_dialog.camera_id
        self.choosing_camera_dialog.close()
        self.choosing_camera_dialog = None
        self.video_player_widget.enable_camera(camera_id)

    def disconnect_camera(self):
        self.video_player_widget.disable_camera()

    def make_photo(self):
        last_frame_pixmap = self.video_player_widget.last_frame_pixmap
        filepath, _ = QFileDialog.getSaveFileName(None, "Specify path and title for the image", "", "Image (*.jpg)",
                                                  options=QFileDialog.DontUseNativeDialog)
        last_frame_pixmap.save(filepath + ".jpg")
