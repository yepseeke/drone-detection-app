import pyqtgraph as pg
import numpy as np

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout
from PyQt5.QtWidgets import QApplication

from signal_processing import SignalProcessorFromFile


class WidgetPlot(QWidget):
    def __init__(self, background_color, styles, x_label: str, y_label: str, pen_color):
        super().__init__()

        self.values = None

        # Creating widget
        self.plot_graph = pg.PlotWidget()
        layout = QVBoxLayout(self)
        layout.addWidget(self.plot_graph)

        self.pen = pg.mkPen(color=pen_color)
        self.plot_graph.setBackground(background_color)

        self.plot_graph.setLabel("left", y_label, **styles)
        self.plot_graph.setLabel("bottom", x_label, **styles)

    def update_values(self, time_start, time_end):
        pass


class SignalPlot(WidgetPlot):
    def __init__(self, signal_source: str, window_size: int, background_color, styles, x_label: str,
                 y_label: str,
                 pen_color):
        super().__init__(background_color, styles, x_label, y_label, pen_color)

        self.window_size = window_size

        self.audio_processor = SignalProcessorFromFile(signal_source)
        self.audio_processor.read_signal()

        self.time = np.linspace(0, self.window_size, window_size)
        self.values = np.zeros(self.window_size)

        self.line = self.plot_graph.plot(self.time, self.values, pen=self.pen)

    def update_values(self, time_start, time_end):
        left = int(time_start * self.audio_processor.sample_rate)
        right = int(time_end * self.audio_processor.sample_rate)

        data = self.audio_processor.audio_data[left:right]

        if data.shape[0] < self.window_size:
            data = np.pad(data, (0, self.window_size - len(data)), mode='constant', constant_values=0)

        self.values = data[:self.window_size]

    def update_plot(self):
        self.line.setData(self.time, self.values)


class MyApp(QMainWindow):
    def __init__(self, signal_source):
        super().__init__()

        # Defining params for signal plot
        window_size = 2205
        signal_styles = {"color": "black", "font-size": "15px"}
        signal_x_label = "Time(sec)"
        signal_y_label = "Amplitude"
        signal_background = (18, 74, 168)

        pen_color = (0, 0, 0)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.signal_widget = SignalPlot(signal_source, window_size, signal_background, signal_styles,
                                        signal_x_label, signal_y_label, pen_color)
        layout.addWidget(self.signal_widget)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.sample_rate = 44100
        self.current_time = 0
        self.interval = 2205

        # Updating plot
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_data(self):
        # Adding signal values to display
        self.signal_widget.update_values(self.current_time, self.current_time + self.interval / self.sample_rate)
        self.current_time += self.interval / self.sample_rate

    def update_plot(self):
        self.update_data()
        self.signal_widget.update_plot()


if __name__ == '__main__':
    app = QApplication([])
    main = MyApp(r'minus.mp3')
    main.show()

    app.exec()
