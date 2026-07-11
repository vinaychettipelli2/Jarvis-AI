"""
voice/voice_loop.py
"""

from voice.voice_assistant import VoiceAssistant


class VoiceLoop:

    def __init__(self):
        print("Initializing VoiceLoop...")
        self.voice = VoiceAssistant()

    def start(self):

        print("Calling greet()...")
        self.voice.greet()

        print("Greeting finished.")
        print("Entering loop...")

        while True:

            print("Waiting for input...")

            text = input("\nYou (simulate voice): ")

            print(f"You typed: {text}")

            if text.lower() == "exit":
                self.voice.speak("Goodbye Vinay.")
                break

            self.voice.speak(f"You said {text}")