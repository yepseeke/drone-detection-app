import sys
import time

from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer, Qt, QElapsedTimer

from video_processing import VideoProcessor


class VideoPlayer(QMainWindow):
    def __init__(self, source):
        super().__init__()

        self.error = 0

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.video_label = QLabel()
        self.layout.addWidget(self.video_label)

        self.video_processor = VideoProcessor(source)
        self.frame_interval = 1000 / self.video_processor.frame_rate

        self.elapsed_timer = QElapsedTimer()
        self.elapsed_timer.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)

        # self.next_frame_time = self.elapsed_timer.elapsed() + self.frame_interval
        self.current_time = 0
        # print(self.next_frame_time, self.elapsed_timer.elapsed())

    def update_frame(self):
        # self.current_time = self.elapsed_timer.elapsed()
        # print(self.current_time, self.next_frame_time)
        print(self.frame_interval)
        self.error += self.frame_interval - int(self.frame_interval)

        if self.current_time >= self.frame_interval:
            self.current_time = 0
            success, frame = self.video_processor.get_frame()

            if success:
                height, width, channel = frame.shape
                bytes_per_line = channel * width

                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)

                self.video_label.setPixmap(pixmap)
            else:
                self.timer.stop()
                self.video_processor.release()
        else:
            self.current_time += 1
