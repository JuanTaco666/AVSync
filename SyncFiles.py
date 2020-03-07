import moviepy
from moviepy.editor import *
from moviepy.audio.AudioClip import *

from Audio import Audio
from SyncAudio import find_concurrent_pairs


def sync_files(audio_file, video_file):
    high_quality_audio = Audio(audio_file=audio_file)
    video_audio = Audio(audio_file=video_file.audio)

    [video_times, audio_times] = find_concurrent_pairs(video_audio, high_quality_audio)

    for i in range(0, len(video_times)):
        audio_times[i] = high_quality_audio.to_seconds(audio_times[i])
        video_times[i] = video_audio.to_seconds(video_times[i])

    # debug
    for i in range(0, len(video_times)):
        video_time = to_string(video_times[i])
        audio_time = to_string(audio_times[i])
        print("was " + video_time + " but now is " + audio_time)

    adjusted_clips = []
    for i in range(0, len(video_times) - 1):
        clip = video_file.subclip(video_times[i], video_times[i + 1])
        proper_duration = audio_times[i + 1] - audio_times[i]
        accelerated_clip = moviepy.video.fx.all.accel_decel(clip, new_duration=proper_duration, abruptness=0)
        adjusted_clips.append(accelerated_clip)

    adjusted_video = concatenate_videoclips(adjusted_clips)
    write_file = adjusted_video.set_audio(audio_file)
    return write_file


def to_string(seconds):
    if int(seconds) % 60 < 10:
        seconds_str = "0" + str(int(seconds) % 60)
    else:
        seconds_str = str(int(seconds) % 60)
    return str(int(seconds) // 60) + ":" + seconds_str
