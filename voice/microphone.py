"""
voice/microphone.py

Production Microphone Manager

Responsibilities:
- Detect microphone
- Record audio
- Save WAV files
- Return numpy audio arrays

This module NEVER performs:
- Speech Recognition
- AI Calls
- Wake Word Detection
- Text To Speech
"""

import logging
import sounddevice as sd
import soundfile as sf
import numpy as np
from pathlib import Path

logger = logging.getLogger("jarvis.voice")


class MicrophoneManager:
    """
    Handles microphone recording.
    """

    def __init__(
        self,
        device=None,
        sample_rate=16000,
        channels=1,
    ):
        self.device = device
        self.sample_rate = sample_rate
        self.channels = channels

    def list_devices(self):
        """Print all available audio devices."""
        devices = sd.query_devices()

        print("\nAvailable Audio Devices\n")
        print(devices)

        return devices

    def record(self, seconds=5):
        """
        Record audio.

        Returns:
            numpy.ndarray
        """

        logger.info("Recording started")

        audio = sd.rec(
            int(seconds * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32",
            device=self.device,
        )

        sd.wait()

        logger.info("Recording finished")

        return audio

    def save(
        self,
        audio: np.ndarray,
        filename="recording.wav",
    ):
        """
        Save audio to WAV.
        """

        path = Path(filename)

        sf.write(
            path,
            audio,
            self.sample_rate,
        )

        logger.info(f"Saved recording to {path}")

        return path