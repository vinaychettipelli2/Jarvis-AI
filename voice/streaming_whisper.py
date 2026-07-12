"""
voice/streaming_whisper.py

Enterprise Streaming Whisper
"""

from __future__ import annotations

from threading import Lock
from typing import Optional

import numpy as np

from faster_whisper import WhisperModel

from voice.voice_logger import VoiceLogger
from voice.metrics import MetricsCollector
from voice.exceptions import SpeechRecognitionError


class StreamingWhisper:
    """
    Enterprise Streaming Whisper Engine

    Features
    --------
    ✔ Offline
    ✔ Thread Safe
    ✔ Streaming Ready
    ✔ Singleton Model
    ✔ Metrics
    ✔ Production Logging
    """

    _model: Optional[WhisperModel] = None

    def __init__(

        self,

        model_path: str,

        device: str = "cpu",

        compute_type: str = "int8",

        language: str = "en",

        beam_size: int = 5,

        metrics: Optional[MetricsCollector] = None,

    ):

        self.logger = VoiceLogger.get_logger()

        self.metrics = metrics or MetricsCollector()

        self.language = language

        self.beam_size = beam_size

        self.lock = Lock()

        if StreamingWhisper._model is None:

            self.logger.info(

                "Loading Streaming Whisper..."

            )

            StreamingWhisper._model = WhisperModel(

                model_path,

                device=device,

                compute_type=compute_type,

            )

            self.logger.info(

                "Streaming Whisper Ready."

            )

    # ------------------------------------------------------

    @property

    def model(self):

        return StreamingWhisper._model

    # ------------------------------------------------------

    def transcribe(

        self,

        audio: np.ndarray,

    ) -> str:

        if audio is None:

            return ""

        with self.lock:

            try:

                with self.metrics.timer(

                    "streaming_whisper"

                ):

                    segments, info = self.model.transcribe(

                        audio,

                        beam_size=self.beam_size,

                        language=self.language,

                        vad_filter=False,

                    )

                text = " ".join(

                    s.text.strip()

                    for s in segments

                ).strip()

                self.logger.info(

                    f"Streaming STT : {text}"

                )

                return text

            except Exception as exc:

                raise SpeechRecognitionError(

                    str(exc)

                ) from exc

    # ------------------------------------------------------

    def transcribe_chunk(

        self,

        chunk: np.ndarray,

    ) -> str:

        return self.transcribe(

            chunk

        )

    # ------------------------------------------------------

    def flush(self):

        """
        Reserved for future context buffering.
        """
        pass

    # ------------------------------------------------------

    def health(self):

        return {

            "loaded": self.model is not None,

            "language": self.language,

            "beam_size": self.beam_size,

        }