"""
voice/barge_in.py

Enterprise Barge-In Controller
"""

from __future__ import annotations

from threading import Event, Lock

from voice.voice_logger import VoiceLogger
from voice.voice_state import VoiceStateManager, VoiceState
from voice.audio_player import AudioPlayer
from voice.metrics import MetricsCollector


class BargeInController:
    """
    Enterprise Barge-In Controller.

    Features
    --------
    ✔ Interrupt TTS
    ✔ Resume Listening
    ✔ Thread Safe
    ✔ Metrics
    ✔ State Management
    ✔ Production Logging
    """

    def __init__(

        self,

        player: AudioPlayer,

        state: VoiceStateManager,

        metrics: MetricsCollector,

    ):

        self.logger = VoiceLogger.get_logger()

        self.player = player

        self.state = state

        self.metrics = metrics

        self._lock = Lock()

        self._interrupted = Event()

    # ---------------------------------------------------------

    @property
    def interrupted(self):

        return self._interrupted.is_set()

    # ---------------------------------------------------------

    def interrupt(self):

        with self._lock:

            if not self.player.is_playing:

                return False

            self.logger.info(

                "Barge-In detected."

            )

            self.metrics.increment(

                "barge_in_count"

            )

            self.player.stop()

            self.state.transition(

                VoiceState.LISTENING

            )

            self._interrupted.set()

            return True

    # ---------------------------------------------------------

    def clear(self):

        with self._lock:

            self._interrupted.clear()

    # ---------------------------------------------------------

    def wait_until_idle(self):

        if self.player.is_playing:

            self.player.wait()

    # ---------------------------------------------------------

    def should_interrupt(

        self,

        speech_detected: bool,

    ) -> bool:

        if not speech_detected:

            return False

        return self.player.is_playing

    # ---------------------------------------------------------

    def health(self):

        return {

            "interrupted": self.interrupted,

            "playing": self.player.is_playing,

            "state": self.state.current.name,

        }