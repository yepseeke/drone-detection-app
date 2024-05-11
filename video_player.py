import sys
import time

from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer, Qt, QElapsedTimer
from PyQt5 import QtCore

from video_processing import VideoProcessor


class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.error = 0

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.cameraEnabled = False
        self.lastFramePixmap = None

        self.setStyleSheet("background-color: black;")

        self.video_label = QLabel()
        self.video_label.setMinimumSize(1, 1)
        self.video_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.video_label)

        self.video_processor = None

        self.elapsed_timer = QElapsedTimer()
        self.elapsed_timer.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        #self.timer.start(1)

        # self.next_frame_time = self.elapsed_timer.elapsed() + self.frame_interval
        self.current_time = 0
        # print(self.next_frame_time, self.elapsed_timer.elapsed())

    def resizeEvent(self, event):
        if self.cameraEnabled and not self.lastFramePixmap is None:
            scaledPic = self.lastFramePixmap.scaled(self.video_label.width(), self.video_label.height(), Qt.KeepAspectRatio)
            self.video_label.setPixmap(scaledPic)
        QWidget.resizeEvent(self, event)

    def update_frame(self):
        if not self.cameraEnabled:
            return
        # self.current_time = self.elapsed_timer.elapsed()
        # print(self.current_time, self.next_frame_time)
        #print(self.frame_interval)
        self.error += self.frame_interval - int(self.frame_interval)

        if self.current_time >= self.frame_interval:
            self.current_time = 0
            success, frame = self.video_processor.get_frame()

            if success:
                height, width, channel = frame.shape
                bytes_per_line = channel * width

                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                self.lastFramePixmap = QPixmap.fromImage(q_image)
                scaledPic = self.lastFramePixmap.scaled(self.video_label.width(), self.video_label.height(), Qt.KeepAspectRatio)
                self.video_label.setPixmap(scaledPic)
            else:
                self.timer.stop()
                self.video_processor.release()
        else:
            self.current_time += 1
        self.update()

    def enable_camera(self, source):
        self.video_processor = VideoProcessor(source)
        self.frame_interval = 1000 / self.video_processor.frame_rate
        self.cameraEnabled = True
        self.timer.start(1)

    def disable_camera(self):
        self.video_processor.release()
        self.video_processor = None
        self.cameraEnabled = False
        self.lastFramePixmap = None
        self.timer.stop()
        self.video_label.clear()