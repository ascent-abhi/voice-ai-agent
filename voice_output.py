from gtts import gTTS
import os


def speak(text):
    tts = gTTS(text)
    tts.save("response.mp3")

    # Speed up audio (1.4x)
    os.system('ffmpeg -y -i response.mp3 -filter:a "atempo=1.4" fast.mp3')

    os.system("mpg123 fast.mp3")

    os.remove("response.mp3")
    os.remove("fast.mp3")
