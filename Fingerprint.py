import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure,
                                      iterate_structure, binary_erosion)
import hashlib
from operator import itemgetter

IDX_FREQ_I = 0
IDX_TIME_J = 1

######################################################################
# Sampling rate, related to the Nyquist conditions, which affects
# the range frequencies we can detect.
DEFAULT_FS = 44100

######################################################################
# Size of the FFT window, affects frequency granularity
DEFAULT_WINDOW_SIZE = 4096

######################################################################
# Ratio by which each sequential window overlaps the last and the
# next window. Higher overlap will allow a higher granularity of offset
# matching, but potentially more fingerprints.
DEFAULT_OVERLAP_RATIO = 0.5

######################################################################
# Minimum amplitude in spectrogram in order to be considered a peak.
# This can be raised to reduce number of fingerprints, but can negatively
# affect accuracy.
DEFAULT_AMP_MIN = 10

######################################################################
# Number of cells around an amplitude peak in the spectrogram in order
# for Dejavu to consider it a spectral peak. Higher values mean less
# fingerprints and faster matching, but can potentially affect accuracy.
PEAK_NEIGHBORHOOD_SIZE = 20

######################################################################
# Thresholds on how close or far fingerprints can be in time in order
# to be paired as a fingerprint. If your max is too low, higher values of
# DEFAULT_FAN_VALUE may not perform as expected.
MIN_HASH_TIME_DELTA = 0
MAX_HASH_TIME_DELTA = 200

######################################################################
# If True, will sort peaks temporally for fingerprinting;
# not sorting will cut down number of fingerprints, but potentially
# affect performance.
PEAK_SORT = True

######################################################################
# Number of bits to grab from the front of the SHA1 hash in the
# fingerprint calculation. The more you grab, the more memory storage, 
# with potentially lesser collisions of matches.
FINGERPRINT_REDUCTION = 20


class Fingerprint:
    def __init__(self, audio_file=None, points=None, length=None,
                Fs=DEFAULT_FS,
                wsize=DEFAULT_WINDOW_SIZE,
                wratio=DEFAULT_OVERLAP_RATIO,
                amp_min=DEFAULT_AMP_MIN,
                plot=False):
        self.Fs = Fs
        if points is not None and length is not None:
            self.important_points = points
            self.length = length
            return

        self.important_points = []
        if audio_file is not None:
            self.length = audio_file.duration
            channel_samples = audio_file.to_soundarray()[:, 0]

            # FFT the signal and extract frequency components
            arr2D = mlab.specgram(
                channel_samples,
                NFFT=wsize,
                Fs=Fs,
                window=mlab.window_hanning,
                noverlap=int(wsize * wratio))[0]

            # apply log transform since specgram() returns linear array
            arr2D = 10 * np.log10(arr2D)
            arr2D[arr2D == -np.inf] = 0  # replace infs with zeros

            self.length = arr2D.shape[1]

            # find local maxima
            self.important_points = get_2D_peaks(arr2D, plot=plot, amp_min=amp_min)

    def get_length(self):
        return self.length

    def get_Fs(self):
        return self.Fs

    def get_points(self):
        return self.important_points

    # cuts with start_time inclusive and stop_time exclusive
    def cut(self, start_time, stop_time):
        new_length = stop_time - start_time
        new_points = []
        for point in self.important_points:
            if start_time <= point.get_time() < stop_time:
                new_point = [point[0] - start_time, point[1]]
                new_points.append(new_point)
        return Fingerprint(points=new_points, length=new_length)



def get_2D_peaks(arr2D, plot=False, amp_min=DEFAULT_AMP_MIN):
    #  http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.iterate_structure.html#scipy.ndimage.iterate_structure
    struct = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(struct, PEAK_NEIGHBORHOOD_SIZE)

    # find local maxima using our filter shape
    local_max = maximum_filter(arr2D, footprint=neighborhood) == arr2D
    background = (arr2D == 0)
    eroded_background = binary_erosion(background, structure=neighborhood,
                                       border_value=1)

    # Boolean mask of arr2D with True at peaks (Fixed deprecated boolean operator by changing '-' to '^')
    detected_peaks = local_max ^ eroded_background

    # extract peaks
    amps = arr2D[detected_peaks]
    j, i = np.where(detected_peaks)

    # filter peaks
    amps = amps.flatten()
    peaks = zip(i, j, amps)
    peaks_filtered = filter(lambda x: x[2] > amp_min, peaks)  # freq, time, amp
    # get indices for frequency and time
    frequency_idx = []
    time_idx = []
    for x in peaks_filtered:
        frequency_idx.append(x[1])
        time_idx.append(x[0])

    if plot:
        # scatter of the peaks
        fig, ax = plt.subplots()
        ax.imshow(arr2D)
        ax.scatter(time_idx, frequency_idx)
        ax.set_xlabel('Time')
        ax.set_ylabel('Frequency')
        ax.set_title("Spectrogram")
        plt.gca().invert_yaxis()
        plt.show()

    return zip(frequency_idx, time_idx)
