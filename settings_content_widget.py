from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QPushButton, QFileDialog, QFrame, QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from advanced_video_player import AdvancedVideoPlayer
from model import Model

settings_content_widget_path = r'ui/settingsContentWidget.ui'
background_color = (19, 19, 19)
cyan_color = (67, 252, 252)
model_path_1 = r'models/light.pt'
model_path_2 = r'models/heavy1.pt'
model_path_3 = r'models/heavy2.pt'

class SettingsContentWidget(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi(settings_content_widget_path, self)

        self.model = Model()

        self.model_button_1 = self.findChild(QPushButton, "modelButton1")
        self.model_button_1.toggled.connect(self.setFirstModel)
        self.model_button_1.setChecked(True)

        self.model_button_2 = self.findChild(QPushButton, "modelButton2")
        self.model_button_2.toggled.connect(self.setSecondModel)

        self.model_button_3 = self.findChild(QPushButton, "modelButton3")
        self.model_button_3.toggled.connect(self.setThirdModel)


    def setFirstModel(self, flag):
        if flag:
            self.model.set_model(model_path_1)

    def setSecondModel(self, flag):
        if flag:
            self.model.set_model(model_path_2)

    def setThirdModel(self, flag):
        if flag:
            self.model.set_model(model_path_3)
