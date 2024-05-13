from PyQt5.QtCore import QTimer, QElapsedTimer, Qt, pyqtSignal
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage

from video_processing import VideoProcessor

background_color = (0, 0, 0)


class VideoPlayer(QWidget):
    frame_changed_signal = pyqtSignal(int)

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

    def update_frame(self, force_update=False):
        if not self.camera_enabled:
            return

        current_time = self.elapsed_timer.elapsed()

        if current_time >= self.frame_interval or force_update:
            success, frame = self.video_processor.get_annotated_frame()

            if success:
                self.frame_changed_signal.emit(self.video_processor.current_frame_index)

                q_image = self.video_processor.get_QImage(frame)
                self.last_frame_pixmap = QPixmap.fromImage(q_image)

                scaled_frame = self.last_frame_pixmap.scaled(self.video_label.width(), self.video_label.height(),
                                                             Qt.KeepAspectRatio)
                self.video_label.setPixmap(scaled_frame)

                self.elapsed_timer.restart()

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

        # self.timer.stop()
        self.video_label.clear()

    def stop_camera(self):
        self.camera_enabled = False

    def resume_camera(self):
        self.camera_enabled = True

    def total_frames(self):
        return self.video_processor.total_frames

    def move_to_frame(self, index):
        self.video_processor.set_frame_index(index)
