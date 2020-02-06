import numpy as np

from scipy.signal import spectrogram
from scipy.fft import fftshift
import matplotlib.pyplot as plt


class Spectrogram:
    def __init__(self, audio_file, delta_time):
        sound_array = audio_file.to_soundarray()
        # mono_array = []
        # for i in range(len(sound_array)):
        #     mono_array.append(0.5 * (sound_array[0] + sound_array[1]))
        mono_array = sound_array[:, 0]
        f, t, Sxx = spectrogram(mono_array, fs=delta_time)

        plt.pcolormesh(t, f, Sxx)
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.show()

    def get_length(self):
        return self.length

    def get_peaks(self):
        return self.peaks


def show_figure(data, peaks=[]):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=data,
        mode='lines+markers',
        name='Original Plot'
    ))

    fig.add_trace(go.Scatter(
        x=peaks,
        y=[data[j] for j in peaks],
        mode='markers',
        marker=dict(
            size=8,
            color='red',
            symbol='cross'
        ),
        name='Detected Peaks'
    ))

    fig.show()


def get_volume_array(audio, delta_time):
    cut = lambda i: audio.subclip(i * delta_time, i * delta_time + delta_time).to_soundarray(fps=22000)
    volume = lambda array: np.sqrt(((1.0 * array) ** 2).mean())
    volumes = [volume(cut(i)) for i in range(0, int(audio.duration / delta_time - 2))]
    return volumes
