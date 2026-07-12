"""
voice/speech_to_text.py

Production Speech-to-Text using Faster-Whisper.
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

from faster_whisper import WhisperModel

from voice.interfaces import SpeechRecognizer
from voice.exceptions import (
    SpeechRecognitionError,
    AudioFileError,
)
from voice.voice_logger import VoiceLogger


class SpeechToText(SpeechRecognizer):
    """
    Enterprise Speech Recognition.

    Features
    --------
    ✔ Offline
    ✔ Faster-Whisper
    ✔ Production Logging
    ✔ Lazy Model Loading
    ✔ Singleton Model
    ✔ Thread Safe (Read)
    ✔ Input Validation
    ✔ Language Selection
    ✔ Beam Search
    """

    _model = None

    def __init__(
        self,
        model_path: str,
        device: str = "cpu",
        compute_type: str = "int8",
        language: str = "en",
        beam_size: int = 5,
    ):

        self.logger = VoiceLogger.get_logger()

        self.model_path = Path(model_path)

        self.device = device

        self.compute_type = compute_type

        self.language = language

        self.beam_size = beam_size

        self._load_model()

    # ---------------------------------------------------------

    def _load_model(self):

        if SpeechToText._model is not None:
            return

        if not self.model_path.exists():

            raise SpeechRecognitionError(

                f"Whisper model not found: {self.model_path}"

            )

        self.logger.info(

            "Loading Faster-Whisper model..."

        )

        SpeechToText._model = WhisperModel(

            str(self.model_path),

            device=self.device,

            compute_type=self.compute_type,

        )

        self.logger.info(

            "Whisper model loaded successfully."

        )

    # ---------------------------------------------------------

    @property
    def model(self):

        return SpeechToText._model

    # ---------------------------------------------------------

    def transcribe(
        self,
        audio: Path,
    ) -> str:

        if not audio.exists():

            raise AudioFileError(

                f"Audio file not found: {audio}"

            )

        try:

            segments, info = self.model.transcribe(

                str(audio),

                beam_size=self.beam_size,

                language=self.language,

                vad_filter=True,

            )

            text = " ".join(

                segment.text.strip()

                for segment in segments

            ).strip()

            self.logger.info(

                f"Detected Language : {info.language}"

            )

            self.logger.info(

                f"Recognition : {text}"

            )

            return text

        except Exception as exc:

            raise SpeechRecognitionError(

                str(exc)

            ) from exc

    # ---------------------------------------------------------

    @property
    def current_model(self) -> Final[str]:

        return str(self.model_path)