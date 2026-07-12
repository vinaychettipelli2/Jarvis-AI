"""
voice/microphone.py

Production Microphone Manager.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
import sounddevice as sd
import soundfile as sf

from voice.interfaces import Recorder
from voice.exceptions import (
    MicrophoneError,
    RecordingError,
)
from voice.voice_logger import VoiceLogger


class MicrophoneManager(Recorder):
    """
    Enterprise-grade microphone recorder.

    Features
    --------
    ✔ Device validation
    ✔ Automatic WAV saving
    ✔ Configurable sample rate
    ✔ Mono / Stereo support
    ✔ Exception handling
    ✔ Logging
    """

    def __init__(
        self,
        sample_rate: int,
        channels: int,
        device: Optional[int] = None,
        output_file: str = "recording.wav",
    ):

        self.logger = VoiceLogger.get_logger()

        self.sample_rate = sample_rate

        self.channels = channels

        self.device = device

        self.output_file = Path(output_file)

        self._recording = None

        self.validate_device()

    # ---------------------------------------------------------

    def validate_device(self):

        try:

            devices = sd.query_devices()

            if self.device is None:
                return

            if self.device >= len(devices):

                raise MicrophoneError(

                    f"Invalid microphone index: {self.device}"

                )

        except Exception as exc:

            raise MicrophoneError(str(exc)) from exc

    # ---------------------------------------------------------

    def list_devices(self):

        return sd.query_devices()

    # ---------------------------------------------------------

    def start(
        self,
        duration: float = 5.0,
    ) -> None:

        try:

            frames = int(

                duration *

                self.sample_rate

            )

            self.logger.info(

                "Recording started."

            )

            self._recording = sd.rec(

                frames,

                samplerate=self.sample_rate,

                channels=self.channels,

                dtype=np.float32,

                device=self.device,

            )

        except Exception as exc:

            raise RecordingError(

                str(exc)

            ) from exc

    # ---------------------------------------------------------

    def stop(self) -> Path:

        try:

            sd.wait()

            sf.write(

                self.output_file,

                self._recording,

                self.sample_rate,

            )

            self.logger.info(

                f"Recording saved : {self.output_file}"

            )

            return self.output_file

        except Exception as exc:

            raise RecordingError(

                str(exc)

            ) from exc

    # ---------------------------------------------------------

    def record(

        self,

        duration: float = 5.0,

    ) -> Path:

        self.start(duration)

        return self.stop()

    # ---------------------------------------------------------

    @property

    def sample_rate_hz(self):

        return self.sample_rate

    @property

    def output_path(self):

        return self.output_file