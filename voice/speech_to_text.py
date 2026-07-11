"""
voice/speech_to_text.py

Production Speech-to-Text using Faster Whisper.

Responsibilities:
- Load Whisper model once
- Convert WAV -> Text
- Return recognized text
- Never call AI directly
"""

import logging
from pathlib import Path
from faster_whisper import WhisperModel

logger = logging.getLogger("jarvis.voice")


class SpeechToText:

    def __init__(
        self,
        model_size="base",
        device="cpu",
        compute_type="int8",
    ):
        logger.info("Loading Faster Whisper model...")

        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type,
        )

        logger.info("Whisper loaded successfully.")

    def transcribe(self, audio_file: str) -> str:

        audio_path = Path(audio_file)

        if not audio_path.exists():
            raise FileNotFoundError(audio_file)

        segments, info = self.model.transcribe(
            str(audio_path),
            beam_size=5,
        )

        text = ""

        for segment in segments:
            text += segment.text + " "

        text = text.strip()

        logger.info(f"Recognized: {text}")

        return text