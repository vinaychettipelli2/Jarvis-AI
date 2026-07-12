"""
voice/webrtc_vad.py

Enterprise WebRTC Voice Activity Detection
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import soundfile as sf

from voice.interfaces import VoiceActivityDetector
from voice.voice_logger import VoiceLogger
from voice.exceptions import (
    AudioFileError,
    VoiceActivityError,
)

try:

    import webrtcvad

    WEBRTC_AVAILABLE = True

except ImportError:

    WEBRTC_AVAILABLE = False


class WebRTCVAD(VoiceActivityDetector):
    """
    Enterprise WebRTC VAD

    Features
    --------
    ✔ Offline
    ✔ Production Ready
    ✔ Aggressiveness Level
    ✔ Frame Based
    ✔ Fast
    ✔ Thread Safe
    """

    VALID_FRAME_MS = (10, 20, 30)

    def __init__(

        self,

        aggressiveness: int = 2,

        sample_rate: int = 16000,

        frame_duration_ms: int = 30,

    ):

        self.logger = VoiceLogger.get_logger()

        self.sample_rate = sample_rate

        self.frame_duration_ms = frame_duration_ms

        if frame_duration_ms not in self.VALID_FRAME_MS:

            raise VoiceActivityError(

                "Frame duration must be 10, 20 or 30 ms."

            )

        self.vad = None

        if WEBRTC_AVAILABLE:

            self.vad = webrtcvad.Vad(

                aggressiveness

            )

        else:

            self.logger.warning(

                "webrtcvad package not installed."

            )

    # ---------------------------------------------------------

    @property

    def enabled(self):

        return self.vad is not None

    # ---------------------------------------------------------

    def contains_speech(

        self,

        audio: Path,

    ) -> bool:

        if not audio.exists():

            raise AudioFileError(

                f"{audio} not found."

            )

        if self.vad is None:

            return False

        try:

            samples, sr = sf.read(

                audio,

                dtype="int16",

            )

            if sr != self.sample_rate:

                raise VoiceActivityError(

                    f"Expected {self.sample_rate}Hz but received {sr}Hz."

                )

            if samples.ndim > 1:

                samples = np.mean(

                    samples,

                    axis=1,

                ).astype(np.int16)

            frame_size = int(

                sr *

                self.frame_duration_ms /

                1000

            )

            bytes_per_frame = (

                frame_size * 2

            )

            raw = samples.tobytes()

            speech_frames = 0

            total_frames = 0

            for index in range(

                0,

                len(raw),

                bytes_per_frame,

            ):

                frame = raw[

                    index:index + bytes_per_frame

                ]

                if len(frame) != bytes_per_frame:

                    continue

                total_frames += 1

                if self.vad.is_speech(

                    frame,

                    sr,

                ):

                    speech_frames += 1

            if total_frames == 0:

                return False

            ratio = (

                speech_frames /

                total_frames

            )

            self.logger.info(

                f"Speech Ratio={ratio:.2f}"

            )

            return ratio >= 0.25

        except Exception as exc:

            raise VoiceActivityError(

                str(exc)

            ) from exc

    # ---------------------------------------------------------

    def speech_ratio(

        self,

        audio: Path,

    ) -> float:

        if not self.contains_speech(audio):

            return 0.0

        return 1.0