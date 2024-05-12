from video_player import *

class AdvancedVideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.video_player = VideoPlayer()
        self.layout.addWidget(self.video_player)

    def set_video(self, video_path):
        self.video_player.enable_camera(video_path)

    def clear(self):
        self.video_player.disable_camera()