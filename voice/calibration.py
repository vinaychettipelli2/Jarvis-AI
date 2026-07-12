"""
voice/calibration.py

Enterprise Automatic Microphone Calibration
"""

from __future__ import annotations

from dataclasses import dataclass
from threading import Lock

import numpy as np
import sounddevice as sd

from voice.voice_logger import VoiceLogger
from voice.exceptions import MicrophoneError


@dataclass(slots=True)
class CalibrationResult:

    noise_floor: float

    rms: float

    peak: float

    recommended_threshold: float

    duration: float


class MicrophoneCalibrator:
    """
    Enterprise Automatic Microphone Calibration.

    Features
    --------
    ✔ Ambient noise calibration
    ✔ RMS calculation
    ✔ Peak calculation
    ✔ Recommended VAD threshold
    ✔ Thread Safe
    ✔ Production Logging
    """

    def __init__(

        self,

        sample_rate: int,

        channels: int,

        device: int | None = None,

    ):

        self.logger = VoiceLogger.get_logger()

        self.sample_rate = sample_rate

        self.channels = channels

        self.device = device

        self._lock = Lock()

        self._result: CalibrationResult | None = None

    # ---------------------------------------------------------

    def calibrate(

        self,

        seconds: float = 2.0,

    ) -> CalibrationResult:

        with self._lock:

            try:

                self.logger.info(

                    "Calibrating microphone..."

                )

                frames = int(

                    seconds *

                    self.sample_rate

                )

                samples = sd.rec(

                    frames,

                    samplerate=self.sample_rate,

                    channels=self.channels,

                    dtype="float32",

                    device=self.device,

                )

                sd.wait()

                if samples.ndim > 1:

                    samples = np.mean(

                        samples,

                        axis=1,

                    )

                rms = float(

                    np.sqrt(

                        np.mean(

                            samples ** 2

                        )

                    )

                )

                peak = float(

                    np.max(

                        np.abs(samples)

                    )

                )

                noise_floor = float(

                    np.mean(

                        np.abs(samples)

                    )

                )

                threshold = max(

                    noise_floor * 2.5,

                    0.015,

                )

                self._result = CalibrationResult(

                    noise_floor=noise_floor,

                    rms=rms,

                    peak=peak,

                    recommended_threshold=threshold,

                    duration=seconds,

                )

                self.logger.info(

                    "Calibration completed."

                )

                return self._result

            except Exception as exc:

                raise MicrophoneError(

                    str(exc)

                ) from exc

    # ---------------------------------------------------------

    @property

    def result(self):

        return self._result

    # ---------------------------------------------------------

    @property

    def threshold(self):

        if self._result is None:

            return 0.015

        return self._result.recommended_threshold