from video_player import *
from PyQt5.QtWidgets import QSlider

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
        self.layout.addWidget(self.slider, 1)

    def set_video(self, video_path):
        self.video_loaded = True
        self.video_player.enable_camera(video_path)
        self.slider.setMaximum(self.video_player.total_frames())

    def clear(self):
        self.video_loaded = False
        self.video_player.disable_camera()
        self.slider.setMaximum(0)

    def move_to_frame(self):
        if not self.slider_is_pressed:
            return
        index = int(self.slider.value())
        self.video_player.move_to_frame(index)

    def change_slider_state_to_true(self):
        self.slider_is_pressed = True

    def change_slider_state_to_false(self):
        self.slider_is_pressed = False

    def change_slider_position(self, index):
        self.slider.setValue(index)