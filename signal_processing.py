import librosa

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout
from PyQt5.QtWidgets import QApplication
from scipy import signal


class SignalProcessor:
    def __init__(self):
        self.sample_rate = None
        self.audio_data = None


class SignalProcessorFromFile(SignalProcessor):
    def __init__(self, audio_source):
        super().__init__()

        self.audio_source = audio_source

    def read_signal(self):
        self.audio_data, self.sample_rate = librosa.load(self.audio_source, sr=None)

    def get_length(self):
        return self.audio_data.shape[0]

    def get_sample_rate(self):
        return self.sample_rate

    def get_audio_data(self):
        return self.audio_data

    def get_sample(self, sample_start_time, sample_end_time):
        left = int(sample_start_time / 1000 * self.sample_rate)
        right = int(sample_end_time / 1000 * self.sample_rate)
        return self.audio_data[left:right]
