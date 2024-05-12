from video_player import *
from PyQt5.QtWidgets import QSlider, QHBoxLayout, QPushButton
from PyQt5.QtGui import QIcon

pause_icon_path = r'images/pauseIcon.svg'
play_icon_path = r'images/playIcon.svg'

class AdvancedVideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.video_loaded = False

        self.video_player = VideoPlayer()
        self.layout.addWidget(self.video_player, 7)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(0)
        self.slider_is_pressed = False
        self.slider.sliderPressed.connect(self.change_slider_state_to_true)
        self.slider.sliderReleased.connect(self.change_slider_state_to_false)
        self.slider.valueChanged.connect(self.move_to_frame)
        self.video_player.frame_changed_signal.connect(self.change_slider_position)

        self.pause_resume_button = QPushButton()
        self.pause_resume_button_state = False
        self.pause_resume_button_state_temporary = False
        self.pause_resume_button.setText("")
        self.pause_resume_button.setIcon(QIcon(play_icon_path))
        self.pause_resume_button.setStyleSheet("QPushButton{ color: rgb(67, 252, 252); } QPushButton:hover{ color: rgb(67, 252, 252); border: 4px solid rgb(67, 252, 252); }")
        self.pause_resume_button.clicked.connect(self.change_pause_resume_button_state)

        self.slider_pause_layout = QHBoxLayout()
        self.slider_pause_layout.addWidget(self.slider, 9)
        self.slider_pause_layout.addWidget(self.pause_resume_button, 1)
        self.layout.addLayout(self.slider_pause_layout, 1)

    def set_video(self, video_path):
        self.video_loaded = True
        self.video_player.enable_camera(video_path)
        self.slider.setMaximum(self.video_player.total_frames())
        self.pause_resume_button_state = True
        self.pause_resume_button_state_temporary = True
        self.pause_resume_button.setIcon(QIcon(pause_icon_path))

    def clear(self):
        self.video_loaded = False
        self.video_player.disable_camera()
        self.slider.setMaximum(0)
        self.pause_resume_button_state = False
        self.pause_resume_button_state_temporary = False
        self.pause_resume_button.setIcon(QIcon(play_icon_path))

    def move_to_frame(self):
        if not self.slider_is_pressed:
            return
        index = int(self.slider.value())
        self.video_player.move_to_frame(index)

    def change_slider_state_to_true(self):
        self.slider_is_pressed = True
        if not self.pause_resume_button_state_temporary:
            self.video_player.resume_camera()
        #self.stop_player()

    def change_slider_state_to_false(self):
        self.slider_is_pressed = False
        if not self.pause_resume_button_state_temporary:
            self.video_player.stop_camera()
        #self.resume_player()

    def change_slider_position(self, index):
        self.slider.setValue(index)

    def change_pause_resume_button_state(self):
        if self.pause_resume_button_state:
            self.stop_player()
        else:
            self.resume_player()

    def stop_player(self):
        self.pause_resume_button_state = False
        self.pause_resume_button_state_temporary = False
        self.video_player.stop_camera()
        self.pause_resume_button.setIcon(QIcon(play_icon_path))

    def resume_player(self):
        self.pause_resume_button_state = True
        self.pause_resume_button_state_temporary = True
        self.video_player.resume_camera()
        self.pause_resume_button.setIcon(QIcon(pause_icon_path))