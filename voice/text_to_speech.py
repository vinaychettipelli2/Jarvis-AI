"""
voice/text_to_speech.py

Production Offline Text-to-Speech using Piper.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional

from voice.interfaces import SpeechSynthesizer
from voice.exceptions import (
    SpeechSynthesisError,
    ConfigurationError,
)
from voice.voice_logger import VoiceLogger


class TextToSpeech(SpeechSynthesizer):
    """
    Enterprise Piper TTS.

    Features
    --------
    ✔ Offline
    ✔ Production Logging
    ✔ Input Validation
    ✔ Output Validation
    ✔ Configurable Voice
    ✔ Configurable Output
    ✔ Interface Based
    """

    def __init__(
        self,
        piper_path: str,
        voice_path: str,
        output_file: str = "jarvis_output.wav",
    ):

        self.logger = VoiceLogger.get_logger()

        self.piper = Path(piper_path)

        self.voice = Path(voice_path)

        self.output = Path(output_file)

        self._validate()

    # ---------------------------------------------------------

    def _validate(self):

        if not self.piper.exists():

            raise ConfigurationError(

                f"Piper executable not found : {self.piper}"

            )

        if not self.voice.exists():

            raise ConfigurationError(

                f"Voice model not found : {self.voice}"

            )

    # ---------------------------------------------------------

    def synthesize(self, text: str) -> Path:

        if not text:

            raise SpeechSynthesisError(

                "Cannot synthesize empty text."

            )

        try:

            if self.output.exists():

                self.output.unlink()

            subprocess.run(

                [

                    str(self.piper),

                    "--model",

                    str(self.voice),

                    "--output_file",

                    str(self.output),

                ],

                input=text,

                text=True,

                check=True,

                capture_output=True,

            )

            if not self.output.exists():

                raise SpeechSynthesisError(

                    "Piper did not generate output."

                )

            self.logger.info(

                f"TTS completed ({len(text)} chars)."

            )

            return self.output

        except subprocess.CalledProcessError as exc:

            raise SpeechSynthesisError(

                exc.stderr or str(exc)

            ) from exc

        except Exception as exc:

            raise SpeechSynthesisError(

                str(exc)

            ) from exc

    # ---------------------------------------------------------

    @property
    def voice_model(self) -> Path:

        return self.voice

    @property
    def output_file(self) -> Path:

        return self.output