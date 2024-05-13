from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QPushButton, QFileDialog, QFrame, QWidget, QVBoxLayout, QSpacerItem, QSizePolicy

from choosing_camera_dialog import ChoosingCameraDialog
from video_player import VideoPlayer

background_color = (19, 19, 19)
cyan_color = (67, 252, 252)

class CameraContentWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(f"background-color: rgb{background_color};")

        self.main_layout = QVBoxLayout()
        self.video_player_widget = VideoPlayer()
        self.main_layout.addWidget(self.video_player_widget, 9)

        self.buttons_layout = QHBoxLayout()

        self.choosing_camera_dialog = None

        self.choose_camera_button = QPushButton()
        self.choose_camera_button.setText("Выбрать камеру")
        self.choose_camera_button.setMinimumHeight(50)
        self.choose_camera_button.setStyleSheet("QPushButton{color: rgb(67, 252, 252);border: 4px solid rgb(67, 252, 252);border-radius: 10px;font-size: 12pt;} QPushButton:hover{background-color:rgb(0,255,0); color: rgb(0, 0, 0);}")
        self.choose_camera_button.clicked.connect(self.choose_camera)

        self.disconnect_camera_button = QPushButton()
        self.disconnect_camera_button.setText("Отключить камеру")
        self.disconnect_camera_button.setMinimumHeight(50)
        self.disconnect_camera_button.setStyleSheet("QPushButton{color: rgb(67, 252, 252);border: 4px solid rgb(67, 252, 252);border-radius: 10px;font-size: 12pt;} QPushButton:hover{background-color:rgb(0,255,0); color: rgb(0, 0, 0);}")
        self.disconnect_camera_button.clicked.connect(self.disconnect_camera)

        self.make_photo_button = QPushButton()
        self.make_photo_button.setText("Сделать снимок")
        self.make_photo_button.setMinimumHeight(50)
        self.make_photo_button.setStyleSheet("QPushButton{color: rgb(67, 252, 252);border: 4px solid rgb(67, 252, 252);border-radius: 10px;font-size: 12pt;} QPushButton:hover{background-color:rgb(0,255,0); color: rgb(0, 0, 0);}")
        self.make_photo_button.clicked.connect(self.make_photo)

        self.buttons_layout.addWidget(self.choose_camera_button, 1)
        self.buttons_layout.addWidget(self.disconnect_camera_button, 1)
        self.buttons_layout.addWidget(self.make_photo_button, 1)
        space_widget_1 = QWidget()
        self.buttons_layout.addWidget(space_widget_1, 2)

        self.main_layout.addLayout(self.buttons_layout, 1)
        self.setLayout(self.main_layout)

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

