import time
from PyQt5.QtCore import QTimer, QElapsedTimer
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QPixmap, QImage
from video_processing import VideoProcessor


class VideoPlayer(QMainWindow):
    def __init__(self, source):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.video_label = QLabel()
        self.layout.addWidget(self.video_label)

        self.video_processor = VideoProcessor(source)
        self.frame_rate = self.video_processor.frame_rate
        self.frame_interval = 1000 / self.frame_rate

        self.elapsed_timer = QElapsedTimer()
        self.elapsed_timer.start()

        self.timer = QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start()

    def update_frame(self):
        current_time = self.elapsed_timer.elapsed()

        if current_time >= self.frame_interval:
            success, frame = self.video_processor.get_annotated_frame()

            if success:
                height, width, channel = frame.shape
                bytes_per_line = channel * width

                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)

                self.video_label.setPixmap(pixmap)

                self.elapsed_timer.restart()
            else:
                self.timer.stop()
                self.video_processor.release()
