from moviepy.editor import *

from SyncFiles import sync_files


video_file = VideoFileClip("Examples/mfaf_video.mp4")
audio_file = AudioFileClip("Examples/mfaf_audio.wav")

video_with_audio = sync_files(audio_file, video_file)
video_with_audio.write_videofile("adjusted_video.mp4")
