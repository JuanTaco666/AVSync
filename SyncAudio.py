from AudioCompare import compare_clips

clip_radius = 25


# Very naive, and should be changed
def find_concurrent_pairs(compared_audio, audio):
    concurrent_pairs = [[], []]
    concurrent_pairs[0].append(0)  # compared_audio start
    concurrent_pairs[1].append(0)  # audio_start

    for i in range(clip_radius, audio.get_length() - clip_radius, 2 * clip_radius):
        concurrent_pairs[1].append(i)

        clip = audio.cut(i - clip_radius, i + clip_radius)

        best_time = 0
        best_cost = float("inf")
        for j in range(clip_radius, compared_audio.get_length() - clip_radius, 1):
            compared_clip = compared_audio.cut(j - clip_radius, j + clip_radius)
            cost = compare_clips(clip, compared_clip)
            if cost < best_cost:
                best_cost = cost
                best_time = j
        concurrent_pairs[0].append(best_time)

    concurrent_pairs[0].append(compared_audio.get_length())
    concurrent_pairs[1].append(audio.get_length())

    return concurrent_pairs


def is_sorted(data):
    for i in range(1, len(data)):
        if data[i - 1] > data[i]:
            return False
    return True


# Might need changing
def out_of_order_indices(data):
    if is_sorted(data):
        return []
    worst_cost = 0.0
    worst_index = 0
    for i in range(0, len(data)):
        cost = 0
        for j in range(0, i):
            if data[j] > data[i]:
                cost += 1
        for j in range(i + 1, len(data)):
            if data[j] < data[i]:
                cost += 1
        if cost > worst_cost:
            worst_index = i
            worst_cost = cost
    copy = list.copy(data)
    copy.pop(worst_index)
    indices_to_remove = out_of_order_indices(copy)
    for i in range(0, len(indices_to_remove)):
        if worst_index <= indices_to_remove[i]:
            indices_to_remove[i] += 1
    indices_to_remove.append(worst_index)
    return indices_to_remove


def remove_unordered_pairs(pairs):
    indices_to_remove = out_of_order_indices(pairs[0])
    indices_to_remove.sort(reverse=True)
    for i in indices_to_remove:
        pairs[0].pop(i)
        pairs[1].pop(i)
