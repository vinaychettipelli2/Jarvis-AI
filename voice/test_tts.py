from voice.text_to_speech import TextToSpeech
from voice.audio_player import AudioPlayer

tts = TextToSpeech(
    piper_path="C:/AI/piper/piper.exe",
    voice_path="C:/AI/piper/voices/en_US-lessac-medium.onnx",
)

tts.speak("Hello Vinay. I am Jarvis.")

player = AudioPlayer()
player.play("jarvis_output.wav")