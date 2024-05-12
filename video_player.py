import time
import sys

from PyQt5.QtCore import QTimer, QElapsedTimer, Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage

from video_processing import VideoProcessor

background_color = (0, 0, 0)


class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.setStyleSheet(f'background-color: rgb{background_color};')

        self.video_label = QLabel()
        self.video_label.setMinimumSize(1, 1)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.video_label)

        self.video_processor = None
        self.last_frame_pixmap = None
        self.camera_enabled = False
        self.frame_interval = 0

        self.elapsed_timer = QElapsedTimer()
        self.elapsed_timer.start()

        self.timer = QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start()

    def update_frame(self):
        if not self.camera_enabled:
            return

        current_time = self.elapsed_timer.elapsed()

        if current_time >= self.frame_interval:
            success, frame = self.video_processor.get_annotated_frame()

            if success:
                height, width, channel = frame.shape
                bytes_per_line = channel * width

                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                self.last_frame_pixmap = QPixmap.fromImage(q_image)
                scaled_frame = self.last_frame_pixmap.scaled(self.video_label.width(), self.video_label.height(),
                                                             Qt.KeepAspectRatio)

                self.video_label.setPixmap(scaled_frame)

                self.elapsed_timer.restart()
            #else:
                #self.timer.stop()
                #self.video_processor.release()


    def resizeEvent(self, event):
        if self.camera_enabled and self.last_frame_pixmap is not None:
            scaled_frame = self.lastFramePixmap.scaled(self.video_label.width(), self.video_label.height(),
                                                       Qt.KeepAspectRatio)
            self.video_label.setPixmap(scaled_frame)
        QWidget.resizeEvent(self, event)

    def enable_camera(self, source):
        self.video_processor = VideoProcessor(source)
        self.frame_interval = 1000 / self.video_processor.frame_rate
        self.camera_enabled = True

    def disable_camera(self):
        self.camera_enabled = False
        self.last_frame_pixmap = None

        self.video_processor.release()
        self.video_processor = None

        #self.timer.stop()
        self.video_label.clear()
