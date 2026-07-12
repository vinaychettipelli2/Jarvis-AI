"""
voice/audio_pipeline.py

Enterprise Audio Pipeline

Responsibilities
----------------
✔ Microphone
✔ Calibration
✔ Voice Activity Detection
✔ Wake Word Detection
✔ Speech Recognition
✔ Metrics
✔ Events
✔ Session

No AI.
No TTS.
No UI.
"""

from __future__ import annotations

from pathlib import Path

from voice.voice_logger import VoiceLogger
from voice.metrics import MetricsCollector
from voice.events import (
    VoiceEvent,
    VoiceEventType,
)
from voice.session import ConversationSession
from voice.calibration import MicrophoneCalibrator
from voice.interfaces import (
    Recorder,
    SpeechRecognizer,
    VoiceActivityDetector,
)
from voice.wake_word import WakeWordDetector


class AudioPipeline:

    """
    Enterprise Audio Pipeline.

    Flow

        Recorder
            ↓
        Calibration
            ↓
        Voice Activity Detection
            ↓
        Wake Word
            ↓
        Speech Recognition
            ↓
        Text
    """

    def __init__(

        self,

        recorder: Recorder,

        recognizer: SpeechRecognizer,

        vad: VoiceActivityDetector,

        wake_word: WakeWordDetector,

        calibrator: MicrophoneCalibrator,

        metrics: MetricsCollector,

        session: ConversationSession,

    ):

        self.logger = VoiceLogger.get_logger()

        self.recorder = recorder

        self.recognizer = recognizer

        self.vad = vad

        self.wake_word = wake_word

        self.calibrator = calibrator

        self.metrics = metrics

        self.session = session

    # --------------------------------------------------------

    def initialize(self):

        """
        Calibrate microphone before starting.
        """

        self.logger.info(

            "Initializing Audio Pipeline..."

        )

        self.calibrator.calibrate()

        self.metrics.increment(

            "calibration_count"

        )

        self.publish(

            VoiceEventType.SYSTEM_STARTED

        )

    # --------------------------------------------------------

    def listen(self):

        """
        Capture user speech.

        Returns
        -------
        str | None
        """

        with self.metrics.timer(

            "record_time"

        ):

            audio = self.recorder.record(

                duration=5

            )

        if not self.vad.contains_speech(

            audio

        ):

            self.metrics.increment(

                "silence_count"

            )

            self.publish(

                VoiceEventType.SILENCE_DETECTED

            )

            return None

        self.publish(

            VoiceEventType.SPEECH_DETECTED

        )

        with self.metrics.timer(

            "transcription"

        ):

            text = self.recognizer.transcribe(

                audio

            )

        if not text:

            return None

        if not self.wake_word.detect(

            text

        ):

            return None

        self.metrics.increment(

            "wakeword_count"

        )

        self.publish(

            VoiceEventType.WAKE_WORD_DETECTED

        )

        self.session.touch()

        return text

    # --------------------------------------------------------

    def shutdown(self):

        self.publish(

            VoiceEventType.SYSTEM_STOPPED

        )

        self.logger.info(

            "Audio Pipeline stopped."

        )

    # --------------------------------------------------------

    def publish(

        self,

        event: VoiceEventType,

    ):

        evt = VoiceEvent(

            event_type=event

        )

        self.logger.info(

            f"EVENT : {evt.event_type.name}"

        )