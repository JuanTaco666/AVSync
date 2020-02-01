from Spectrogram import Spectrogram
from Fingerprint import Fingerprint


class Audio:
    def __init__(self, audio_file=None, fingerprint=None, delta_time=0.01):
        if fingerprint is not None:
            self.fingerprint = fingerprint
        # delta_time is the amount of time between each bit of data: essentially the resolution
        self.delta_time = delta_time
        if audio_file is not None:
            spectrogram = Spectrogram(audio_file, delta_time)
            self.fingerprint = Fingerprint(spectrogram)

    def get_delta_time(self):
        return self.delta_time

    def get_fingerprint(self):
        return self.fingerprint

    def get_length(self):
        return self.get_fingerprint().get_length()

    def cut(self, start_time=0, stop_time=None):
        if stop_time is None:
            stop_time = self.get_length
        cut_fingerprint = self.get_fingerprint().cut(start_time, stop_time)
        return Audio(fingerprint=cut_fingerprint, delta_time=self.delta_time)
