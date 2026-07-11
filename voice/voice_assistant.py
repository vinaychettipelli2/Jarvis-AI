"""
voice/voice_assistant.py

Central controller for all voice operations.
"""

from voice.microphone import MicrophoneManager
from voice.text_to_speech import TextToSpeech
from voice.audio_player import AudioPlayer


class VoiceAssistant:

    def __init__(self):

        self.microphone = MicrophoneManager()

        self.tts = TextToSpeech(
            piper_path="C:/AI/piper/piper.exe",
            voice_path="C:/AI/piper/voices/en_US-lessac-medium.onnx",
        )

        self.player = AudioPlayer()

    def speak(self, text: str):

        self.tts.speak(text)

        self.player.play("jarvis_output.wav")

    def record(self, seconds=5):

        return self.microphone.record(seconds)

    def greet(self):

        self.speak("Hello Vinay. I am Jarvis.")