class FrequencyPoint:
    def __init__(self, time=0, frequency=0):
        self.time = time
        self.frequency = frequency

    def get_time(self):
        return self.time

    def get_frequency(self):
        return self.frequency


class Fingerprint:
    def __init__(self, spectrogram=None, points=None, length=None):
        if points is not None and length is not None:
            self.important_points = points
            self.length = length
            return

        self.important_points = []
        if spectrogram is not None:
            # should be redone!
            for t in spectrogram.get_peaks():
                self.important_points.append(FrequencyPoint(time=t))
            self.length = spectrogram.get_length()

    def get_length(self):
        return self.length

    def get_points(self):
        return self.important_points

    # cuts with start_time inclusive and stop_time exclusive
    def cut(self, start_time, stop_time):
        new_length = stop_time - start_time
        new_points = []
        for point in self.important_points:
            if start_time <= point.get_time() < stop_time:
                new_points.append(point)
        return Fingerprint(points=new_points, length=new_length)
