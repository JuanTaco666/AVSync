import moviepy
from moviepy.editor import *
from moviepy.audio.AudioClip import *

from Audio import Audio
from SyncAudio import find_concurrent_pairs


def sync_files(audio_file, video_file):
    high_quality_audio = Audio(audio_file)
    low_quality_audio = Audio(video_file.audio)

    concurrent_audio_pairs = find_concurrent_pairs(low_quality_audio, high_quality_audio)

    adjusted_clips = []
    for i in range(0, len(concurrent_audio_pairs) - 1):
        clip = video_file.subclip(concurrent_audio_pairs[0][i], concurrent_audio_pairs[0][i + 1])
        proper_duration = concurrent_audio_pairs[1][i + 1] - concurrent_audio_pairs[1][i]
        accelerated_clip = moviepy.video.fx.all.accel_decel(clip, new_duration=proper_duration, abruptness=0)
        adjusted_clips.append(accelerated_clip)

        # debug
        lq_time = concurrent_audio_pairs[0][i + 1]
        hq_time = concurrent_audio_pairs[1][i + 1]
        lq_str = to_string(to_seconds(lq_time, low_quality_audio))
        hq_str = to_string(to_seconds(hq_time, high_quality_audio))
        print("was: " + lq_str + " but now is " + hq_str)

    adjusted_video = concatenate_videoclips(adjusted_clips)
    write_file = adjusted_video.set_audio(audio_file)
    return write_file


def to_seconds(time, audio):
    return time / audio.delta_time


def to_string(seconds):
    if int(seconds) % 60 < 10:
        seconds_str = "0" + str(int(seconds) % 60)
    else:
        seconds_str = str(int(seconds) % 60)
    return str(int(seconds) // 60) + ":" + seconds_str
