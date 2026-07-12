"""
voice/interfaces.py

Enterprise Voice Interfaces
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


# ==========================================================
# Recorder
# ==========================================================

class Recorder(ABC):

    @abstractmethod
    def record(self, duration: int = 5):
        pass


# ==========================================================
# Speech Recognition
# ==========================================================

class SpeechRecognizer(ABC):

    @abstractmethod
    def transcribe(self, audio: Path) -> str:
        pass


# ==========================================================
# Speech Synthesis
# ==========================================================

class SpeechSynthesizer(ABC):

    @abstractmethod
    def synthesize(self, text: str) -> Path:
        pass


# ==========================================================
# Audio Output
# ==========================================================

class AudioOutput(ABC):

    @abstractmethod
    def play(self, audio: Path):
        pass


# ==========================================================
# Voice Activity Detection
# ==========================================================

class VoiceActivityDetector(ABC):

    @abstractmethod
    def contains_speech(self, audio: Path) -> bool:
        pass


# ==========================================================
# Wake Word
# ==========================================================

class WakeWordDetector(ABC):

    @abstractmethod
    def detect(self, data: Any) -> bool:
        pass

    @abstractmethod
    def reset(self):
        pass