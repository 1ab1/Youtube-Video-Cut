import imageio
imageio.plugins.ffmpeg.download()


ffmpeg -ss 16955 -i $(youtube-dl --no-check-certificate -f 22 --get-url https://www.youtube.com/watch?v=nQxS_oYJx3Q) -t 70 -c:v copy -c:a copy react-spot.mp4
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
ffmpeg_extract_subclip("/Users/akkaiah.jagarlamudi/Downloads/Chalapathi.mp4", '00;30', "00:50", targetname="test.mp4")