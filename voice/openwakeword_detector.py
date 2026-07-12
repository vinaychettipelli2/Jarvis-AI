"""
voice/openwakeword_detector.py

Enterprise OpenWakeWord Detector
"""

from __future__ import annotations

from pathlib import Path
from threading import Lock
from typing import Optional

import numpy as np

from voice.voice_logger import VoiceLogger
from voice.exceptions import WakeWordError


try:
    from openwakeword.model import Model

    OPEN_WAKE_WORD_AVAILABLE = True

except ImportError:

    OPEN_WAKE_WORD_AVAILABLE = False

    Model = None


class OpenWakeWordDetector:
    """
    Enterprise OpenWakeWord Wrapper.

    Features
    --------
    ✔ Offline
    ✔ Thread Safe
    ✔ Confidence Threshold
    ✔ Statistics
    ✔ Graceful Fallback
    ✔ Production Logging
    """

    def __init__(

        self,

        model_path: str,

        wake_word: str = "jarvis",

        threshold: float = 0.50,

    ):

        self.logger = VoiceLogger.get_logger()

        self.threshold = threshold

        self.wake_word = wake_word

        self.lock = Lock()

        self.total_frames = 0

        self.total_detections = 0

        self.model = None

        if not OPEN_WAKE_WORD_AVAILABLE:

            self.logger.warning(

                "OpenWakeWord package not installed."

            )

            return

        path = Path(model_path)

        if not path.exists():

            self.logger.warning(

                f"Wake model not found : {path}"

            )

            return

        try:

            self.model = Model(

                wakeword_models=[

                    str(path)

                ]

            )

            self.logger.info(

                "OpenWakeWord initialized."

            )

        except Exception as exc:

            raise WakeWordError(

                str(exc)

            ) from exc

    # ---------------------------------------------------------

    @property

    def enabled(self):

        return self.model is not None

    # ---------------------------------------------------------

    def reset(self):

        if self.model:

            self.model.reset()

    # ---------------------------------------------------------

    def detect(

        self,

        audio_chunk: np.ndarray,

    ) -> bool:

        if self.model is None:

            return False

        try:

            with self.lock:

                prediction = self.model.predict(

                    audio_chunk

                )

                self.total_frames += 1

                if not prediction:

                    return False

                score = prediction.get(

                    self.wake_word,

                    0.0,

                )

                if score >= self.threshold:

                    self.total_detections += 1

                    self.logger.info(

                        f"Wake Word Detected ({score:.2f})"

                    )

                    return True

                return False

        except Exception as exc:

            raise WakeWordError(

                str(exc)

            ) from exc

    # ---------------------------------------------------------

    @property

    def statistics(self):

        return {

            "frames": self.total_frames,

            "detections": self.total_detections,

            "enabled": self.enabled,

        }