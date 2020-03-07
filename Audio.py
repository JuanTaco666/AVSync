from Fingerprint import Fingerprint


class Audio:
    def __init__(self, audio_file=None, fingerprint=None):
        if fingerprint is not None:
            self.fingerprint = fingerprint
        if audio_file is not None:
            self.fingerprint = Fingerprint(audio_file, amp_min=-90, plot=True)

    def get_fingerprint(self):
        return self.fingerprint

    def get_length(self):
        return self.fingerprint.get_length()

    def to_seconds(self, time):
        return self.fingerprint.to_seconds(time)

    def cut(self, start_time=0, stop_time=None):
        if stop_time is None:
            stop_time = self.length
        cut_fingerprint = self.fingerprint.cut(start_time, stop_time)
        return Audio(fingerprint=cut_fingerprint)
