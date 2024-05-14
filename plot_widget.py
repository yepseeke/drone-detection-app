import pyqtgraph as pg
import numpy as np

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout
from PyQt5.QtWidgets import QApplication

from signal_processing import SignalProcessorFromAudioFile, SignalProcessorFromVideoFile, SignalProcessor


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
    def __init__(self, audio_processor: SignalProcessor, window_size: int, background_color, styles, x_label: str,
                 y_label: str, pen_color):
        super().__init__(background_color, styles, x_label, y_label, pen_color)

        self.window_size = window_size

        self.audio_processor = audio_processor

        self.time = np.linspace(0, self.window_size, window_size)
        self.values = np.zeros(self.window_size)

        self.line = self.plot_graph.plot(self.time, self.values, pen=self.pen)

    def update_values(self, start_time, end_time):
        self.audio_processor.read_signal(start_time, end_time)
        data = self.audio_processor.get_audio_data()

        if data.shape[0] < self.window_size:
            data = np.pad(data, (0, self.window_size - len(data)), mode='constant', constant_values=0)

        self.values = data[:self.window_size]

    def update_plot(self):
        self.plot_graph.setYRange(-1, 1)
        self.line.setData(self.time, self.values)


class FFTPlot(WidgetPlot):
    def __init__(self, audio_processor: SignalProcessor, interval: int, background_color, styles, x_label: str,
                 y_label: str, pen_color, plot_type='log'):
        super().__init__(background_color, styles, x_label, y_label, pen_color)

        self.audio_processor = audio_processor
        self.interval = interval
        self.plot_type = plot_type

        sample_rate = self.audio_processor.sample_rate

        # Creating array of frequencies
        self.freqs = np.linspace(0, sample_rate // 2, interval // 2)

        # Defining zero values for the amplitude spectrum
        self.values = np.zeros(interval // 2)

        # Plot data
        self.line = self.plot_graph.plot(self.freqs, self.values, pen=self.pen)

    def update_values(self, time_start, time_end):
        self.values = self.audio_processor.get_fft_data()[:self.interval]
        print(self.values)

    def update_plot(self):
        self.line.setData(self.freqs, self.values)
        if self.plot_type == 'log':
            self.plot_graph.setYRange(-50, 70)
            self.plot_graph.setLogMode(x=True)
        else:
            self.plot_graph.setYRange(-30, 40)


class MyApp(QMainWindow):
    def __init__(self, signal_source):
        super().__init__()

        # Defining params for signal plot
        window_size = 2205
        signal_styles = {"color": "black", "font-size": "15px"}
        signal_x_label = "Time(sec)"
        signal_y_label = "Amplitude"
        signal_background = (18, 74, 168)

        fft_styles = {"color": "black", "font-size": "15px"}
        fft_x_label = "Frequency [Hz]"
        fft_y_label = "PSD [dB]"
        fft_background = (255, 161, 0)

        pen_color = (0, 0, 0)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.audio_processor = SignalProcessorFromVideoFile(signal_source)

        self.signal_widget = SignalPlot(self.audio_processor, window_size, signal_background, signal_styles,
                                        signal_x_label, signal_y_label, pen_color)
        self.fft_widget = FFTPlot(self.audio_processor, window_size, fft_background, fft_styles, fft_x_label,
                                  fft_y_label, pen_color, plot_type='log')

        layout.addWidget(self.signal_widget)
        layout.addWidget(self.fft_widget)

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
        self.fft_widget.update_values(self.current_time, self.current_time + self.interval / self.sample_rate)
        self.current_time += self.interval / self.sample_rate

    def update_plot(self):
        self.update_data()
        self.signal_widget.update_plot()
        self.fft_widget.update_plot()


if __name__ == '__main__':
    app = QApplication([])
    main = MyApp(r'8.mp4')
    main.show()

    app.exec()
