import numpy as np
from scipy.signal import find_peaks
from scipy.signal import find_peaks_cwt
from scipy.signal import savgol_filter

import plotly.graph_objects as go
import pandas as pd


class Spectrogram:
    def __init__(self, audio_file, delta_time):
        # temporary: should be redone!!
        volumes = get_volume_array(audio_file, delta_time)
        show_figure(volumes)
        volumes = savgol_filter(np.array(volumes), 41, 5)
        # self.peaks = find_peaks(volumes, distance=15)
        self.peaks = find_peaks_cwt(volumes, np.arange(1, 16), max_distances=np.arange(1, 16) * 2)
        self.peaks = np.array(self.peaks) - 1
        self.length = len(volumes)

        show_figure(volumes, self.peaks)

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
