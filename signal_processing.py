import librosa
import moviepy.editor as mp
import numpy as np

from scipy.fft import fft


class SignalProcessor:
    def __init__(self):
        self.sample_rate = None
        self.duration = 0
        self.audio_data = []
        self.fft_data = []

    def get_sample_rate(self):
        return self.sample_rate

    def get_audio_data(self):
        return np.array(self.audio_data)

    def get_fft_data(self):
        return np.array(self.fft_data)

    def get_length(self):
        return len(self.audio_data)


# Currently doesn't work
class SignalProcessorFromAudioFile(SignalProcessor):
    def __init__(self, audio_source):
        super().__init__()

        self.audio_source = audio_source

    def read_signal(self):
        self.audio_data, self.sample_rate = librosa.load(self.audio_source, sr=None)

    def get_sample(self, sample_start_time, sample_end_time):
        left = int(sample_start_time / 1000 * self.sample_rate)
        right = int(sample_end_time / 1000 * self.sample_rate)

        if left < 0 or right >= len(self.audio_data):
            raise IndexError('Error: Timings are out of range.')

        return np.array(self.audio_data[left:right])


class SignalProcessorFromVideoFile(SignalProcessor):
    def __init__(self, video_source):
        super().__init__()

        self.video_source = video_source
        self.video = mp.VideoFileClip(self.video_source)
        self.sample_rate = self.video.audio.fps

        self.duration = 0

    def read_signal(self, start_time, end_time):
        try:
            audio = self.video.audio
            self.duration = self.video.duration

            if start_time < 0 or start_time > self.duration:
                raise ValueError("Time exceeds video duration")

            self.audio_data = audio.subclip(start_time, end_time).to_soundarray()
            self.audio_data = np.mean(self.audio_data, axis=1)

            interval = (end_time - start_time) * self.sample_rate
            self.fft_signal(int(interval))

        except Exception as error:
            print('Error extracting audio from video:', error)

    def fft_signal(self, interval, output_type='dB'):
        epsilon = 1e-7
        self.fft_data = np.abs(fft(self.audio_data, interval))[0:interval // 2] + epsilon
        if output_type == 'dB':
            self.fft_data = 20 * np.log10(self.fft_data)


if __name__ == '__main__':
    sp = SignalProcessorFromVideoFile('3.mp4')
    sp.read_signal(109.89, 109.94)
    arr = sp.get_audio_data()

    print(arr)
