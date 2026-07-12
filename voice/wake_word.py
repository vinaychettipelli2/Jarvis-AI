"""
voice/wake_word.py

Production Wake Word Detection.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from voice.voice_logger import VoiceLogger
from voice.exceptions import WakeWordError


# ==========================================================
# Interface
# ==========================================================

class WakeWordDetector(ABC):

    @abstractmethod
    def detect(self, text: Optional[str]) -> bool:
        pass

    @abstractmethod
    def reset(self):
        pass


# ==========================================================
# Default Implementation
# ==========================================================

class JarvisWakeWordDetector(WakeWordDetector):
    """
    Default wake-word detector.

    Current:
        Text based

    Future:
        OpenWakeWord
        Porcupine
        Silero
    """

    def __init__(
        self,
        wake_word: str = "jarvis",
        ignore_case: bool = True,
    ):

        self.logger = VoiceLogger.get_logger()

        self.wake_word = wake_word

        self.ignore_case = ignore_case

        self.detect_count = 0

    # ------------------------------------------------------

    def detect(
        self,
        text: Optional[str],
    ) -> bool:

        if not text:

            return False

        try:

            sentence = text.strip()

            keyword = self.wake_word

            if self.ignore_case:

                sentence = sentence.lower()

                keyword = keyword.lower()

            detected = keyword in sentence

            if detected:

                self.detect_count += 1

                self.logger.info(

                    f"Wake Word Detected ({self.detect_count})"

                )

            return detected

        except Exception as exc:

            raise WakeWordError(

                str(exc)

            ) from exc

    # ------------------------------------------------------

    def reset(self):

        self.detect_count = 0

    # ------------------------------------------------------

    @property
    def total_detections(self):

        return self.detect_count