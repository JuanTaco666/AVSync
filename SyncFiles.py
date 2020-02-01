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
        clip = video_file.subclip(concurrent_audio_pairs[i][0], concurrent_audio_pairs[i + 1][0])
        proper_duration = concurrent_audio_pairs[i + 1][1] - concurrent_audio_pairs[i][1]
        accelerated_clip = moviepy.video.fx.all.accel_decel(clip, new_duration=proper_duration, abruptness=0)
        adjusted_clips.append(accelerated_clip)

    adjusted_video = concatenate_videoclips(adjusted_clips)
    write_file = adjusted_video.set_audio(audio_file)
    return write_file



