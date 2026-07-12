"""
voice/audio_pipeline.py

CHANGED:
- Wake word now activates a session instead of being required for every utterance.
- Active sessions pass recognized text directly to VoiceManager.
"""

from __future__ import annotations

from voice.voice_logger import VoiceLogger
from voice.metrics import MetricsCollector
from voice.events import VoiceEvent, VoiceEventType
from voice.session import ConversationSession
from voice.calibration import MicrophoneCalibrator
from voice.interfaces import (
    Recorder,
    SpeechRecognizer,
    VoiceActivityDetector,
)
from voice.wake_word import WakeWordDetector


class AudioPipeline:

    def __init__(
        self,
        recorder,
        recognizer,
        vad,
        wake_word,
        calibrator,
        metrics,
        session,
    ):

        self.logger = VoiceLogger.get_logger()

        self.recorder = recorder
        self.recognizer = recognizer
        self.vad = vad
        self.wake_word = wake_word
        self.calibrator = calibrator
        self.metrics = metrics
        self.session = session

    # -----------------------------------------------------

    def initialize(self):

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

    # -----------------------------------------------------

    def listen(self):

        audio = self.recorder.record(duration=5)

        if not self.vad.contains_speech(audio):

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

        text = self.recognizer.transcribe(audio)

        if not text:

            return None

        text = text.strip()

        self.logger.info(
            f"Recognition : {text}"
        )

        # -------------------------------------------------
        # Conversation already active
        # -------------------------------------------------

        if self.session.active:

            self.session.touch()

            return text

        # -------------------------------------------------
        # First activation
        # -------------------------------------------------

        if self.wake_word.detect(text):

            self.metrics.increment(
                "wakeword_count"
            )

            self.publish(
                VoiceEventType.WAKE_WORD_DETECTED
            )

            self.session.start()

            self.session.touch()

            return text

        return None

    # -----------------------------------------------------

    def shutdown(self):

        self.publish(
            VoiceEventType.SYSTEM_STOPPED
        )

        self.logger.info(
            "Audio Pipeline stopped."
        )

    # -----------------------------------------------------

    def publish(
        self,
        event,
    ):

        self.logger.info(
            f"EVENT : {event.name}"
        )