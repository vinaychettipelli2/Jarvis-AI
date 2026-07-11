"""
Offline Text-to-Speech using Piper.
"""

import subprocess
from pathlib import Path


class TextToSpeech:

    def __init__(self, piper_path: str, voice_path: str):
        self.piper_path = Path(piper_path)
        self.voice_path = Path(voice_path)

        if not self.piper_path.exists():
            raise FileNotFoundError(f"Piper not found: {self.piper_path}")

        if not self.voice_path.exists():
            raise FileNotFoundError(f"Voice model not found: {self.voice_path}")

    def speak(self, text: str):

        subprocess.run(
            [
                str(self.piper_path),
                "--model",
                str(self.voice_path),
                "--output_file",
                "jarvis_output.wav",
            ],
            input=text,
            text=True,
            check=True,
        )

        print("Speech generated: jarvis_output.wav")