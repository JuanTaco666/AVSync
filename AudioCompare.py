from Audio import Audio
from math import sqrt
from Fingerprint import FrequencyPoint


# Very naive, and should be changed
def distance(p_1, p_2=FrequencyPoint(0, 0)):
    time_dist = p_1.get_time() - p_2.get_time()
    frequency_dist = p_1.get_frequency() - p_2.get_frequency()
    return sqrt(time_dist ** 2 + frequency_dist ** 2)


def min_distance(p, point_list):
    min_dist = float("inf")
    for other_point in point_list:
        dist = distance(p, other_point)
        if dist < min_dist:
            min_dist = dist
    return min_dist


# Very naive, and should be changed
def compare_clips(audio_1, audio_2):
    if audio_1.get_length() != audio_2.get_length():
        raise Exception("audio clips being compared in compare_clips should be of the same length")

    point_list_1 = audio_1.get_fingerprint().get_points()
    point_list_2 = audio_2.get_fingerprint().get_points()

    number_of_points = len(point_list_1) + len(point_list_2)

    total_cost = 0
    for point in point_list_1:
        total_cost += min_distance(point, point_list_2)
    for point in point_list_2:
        total_cost += min_distance(point, point_list_1)
    total_cost /= number_of_points
    return total_cost
