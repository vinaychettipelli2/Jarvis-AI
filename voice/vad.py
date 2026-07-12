"""
voice/vad.py

Production Voice Activity Detection.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import soundfile as sf

from voice.interfaces import VoiceActivityDetector
from voice.exceptions import (
    AudioFileError,
    VoiceActivityError,
)
from voice.voice_logger import VoiceLogger


class EnergyBasedVAD(VoiceActivityDetector):
    """
    Energy Based Voice Activity Detection.

    Features
    --------
    ✔ Offline
    ✔ Fast
    ✔ Production Logging
    ✔ Configurable Threshold
    ✔ Easy replacement with Silero/WebRTC
    """

    def __init__(
        self,
        energy_threshold: float = 0.015,
        speech_ratio: float = 0.10,
    ):

        self.logger = VoiceLogger.get_logger()

        self.energy_threshold = energy_threshold

        self.speech_ratio = speech_ratio

    # ---------------------------------------------------------

    def contains_speech(
        self,
        audio: Path,
    ) -> bool:

        if not audio.exists():

            raise AudioFileError(

                f"Audio not found : {audio}"

            )

        try:

            samples, _ = sf.read(audio)

            if samples.ndim > 1:

                samples = np.mean(

                    samples,

                    axis=1,

                )

            energy = np.abs(samples)

            speech_frames = np.sum(

                energy > self.energy_threshold

            )

            ratio = speech_frames / len(samples)

            detected = ratio >= self.speech_ratio

            self.logger.info(

                f"Speech Ratio={ratio:.3f} Detected={detected}"

            )

            return detected

        except Exception as exc:

            raise VoiceActivityError(

                str(exc)

            ) from exc

    # ---------------------------------------------------------

    def rms(
        self,
        audio: Path,
    ) -> float:

        samples, _ = sf.read(audio)

        if samples.ndim > 1:

            samples = np.mean(

                samples,

                axis=1,

            )

        return float(

            np.sqrt(

                np.mean(samples ** 2)

            )

        )

    # ---------------------------------------------------------

    def duration(
        self,
        audio: Path,
    ) -> float:

        samples, sr = sf.read(audio)

        return len(samples) / sr