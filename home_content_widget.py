from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QPushButton, QFileDialog, QFrame, QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from advanced_video_player import AdvancedVideoPlayer
from model import Model

home_content_widget_path = r'ui/homeContentWidget.ui'
background_color = (19, 19, 19)
cyan_color = (67, 252, 252)

class HomeContentWidget(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi(home_content_widget_path, self)