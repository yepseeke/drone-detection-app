from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QPushButton, QFileDialog, QFrame, QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from image_monitor_widget import ImageMonitorWidget

background_color = (19, 19, 19)
cyan_color = (67, 252, 252)

class ImageContentWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(f"background-color: rgb{background_color};")

        self.main_layout = QVBoxLayout()
        self.image_monitor_widget = ImageMonitorWidget()
        self.main_layout.addWidget(self.image_monitor_widget, 9)

        self.buttons_layout = QHBoxLayout()

        self.upload_image_button = QPushButton()
        self.upload_image_button.setText("Загрузить картинку")
        self.upload_image_button.setMinimumHeight(50)
        self.upload_image_button.setStyleSheet("QPushButton{color: rgb(67, 252, 252);border: 4px solid rgb(67, 252, 252);border-radius: 10px;font-size: 12pt;} QPushButton:hover{background-color:rgb(0,255,0); color: rgb(0, 0, 0);}")
        self.upload_image_button.clicked.connect(self.upload_image)

        self.clear_monitor_button = QPushButton()
        self.clear_monitor_button.setText("Очистить монитор")
        self.clear_monitor_button.setMinimumHeight(50)
        self.clear_monitor_button.setStyleSheet("QPushButton{color: rgb(67, 252, 252);border: 4px solid rgb(67, 252, 252);border-radius: 10px;font-size: 12pt;} QPushButton:hover{background-color:rgb(0,255,0); color: rgb(0, 0, 0);}")
        self.clear_monitor_button.clicked.connect(self.clear_image_monitor)

        self.buttons_layout.addWidget(self.upload_image_button, 1)
        self.buttons_layout.addWidget(self.clear_monitor_button, 1)
        space_widget_1 = QWidget()
        self.buttons_layout.addWidget(space_widget_1, 3)

        self.main_layout.addLayout(self.buttons_layout, 1)
        self.setLayout(self.main_layout)

    def upload_image(self):
        filepath = QFileDialog.getOpenFileName(self, "Provide path to the image", r"/",
                                               "All files (*);; Jpg Files (*.jpg) ;; PNG Files (*.png);")[0]

        if len(filepath) < 3 or filepath[len(filepath) - 3: len(filepath)] != "jpg" and filepath[len(filepath) - 3: len(
                filepath)] != "png":
            raise Exception("Error: Selected file is not an image.")

        image = QPixmap(filepath)
        self.image_monitor_widget.set_image(image)

    def clear_image_monitor(self):
        self.image_monitor_widget.clear()


