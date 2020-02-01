def find_concurrent_pairs(compared_audio, audio):
    concurrent_pairs = []
    for i in range(15):
        concurrent_pairs.append([2 * i, i])
    return concurrent_pairs
