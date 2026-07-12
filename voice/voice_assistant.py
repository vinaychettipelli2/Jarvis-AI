"""
voice/voice_assistant.py

Enterprise Voice Assistant

Coordinates the complete voice pipeline.
"""

from __future__ import annotations

from voice.audio_pipeline import AudioPipeline
from voice.audio_player import AudioPlayer
from voice.barge_in import BargeInController
from voice.events import (
    VoiceEvent,
    VoiceEventType,
)
from voice.metrics import MetricsCollector
from voice.session import ConversationSession
from voice.voice_logger import VoiceLogger
from voice.voice_state import (
    VoiceState,
    VoiceStateManager,
)


class VoiceAssistant:
    """
    Enterprise Voice Assistant.

    Responsibilities
    ----------------
    ✔ Own Audio Pipeline
    ✔ Session Management
    ✔ Metrics
    ✔ Event Publishing
    ✔ Playback
    ✔ Barge-In
    ✔ Voice State

    Does NOT

    ✘ Call AI directly

    ✘ Handle UI

    ✘ Execute Desktop Actions
    """

    def __init__(

        self,

        pipeline: AudioPipeline,

        player: AudioPlayer,

        session: ConversationSession,

        metrics: MetricsCollector,

    ):

        self.logger = VoiceLogger.get_logger()

        self.pipeline = pipeline

        self.player = player

        self.session = session

        self.metrics = metrics

        self.state = VoiceStateManager()

        self.barge = BargeInController(

            player=self.player,

            state=self.state,

            metrics=self.metrics,

        )

    # ---------------------------------------------------------

    def initialize(self):

        self.logger.info(

            "Initializing Voice Assistant."

        )

        self.pipeline.initialize()

        self.session.start()

        self.state.transition(

            VoiceState.IDLE

        )

        self.publish(

            VoiceEventType.SYSTEM_STARTED

        )

    # ---------------------------------------------------------

    def listen(self):

        self.state.transition(

            VoiceState.LISTENING

        )

        text = self.pipeline.listen()

        self.state.transition(

            VoiceState.IDLE

        )

        return text

    # ---------------------------------------------------------

    def speak(

        self,

        synthesizer,

        text: str,

    ):

        if not text:

            return

        self.state.transition(

            VoiceState.SPEAKING

        )

        with self.metrics.timer(

            "tts"

        ):

            audio = synthesizer.synthesize(

                text

            )

        self.player.play(

            audio

        )

        self.state.transition(

            VoiceState.IDLE

        )

        self.publish(

            VoiceEventType.TTS_FINISHED

        )

    # ---------------------------------------------------------

    def interrupt(self):

        return self.barge.interrupt()

    # ---------------------------------------------------------

    def shutdown(self):

        self.logger.info(

            "Voice Assistant Shutdown."

        )

        self.pipeline.shutdown()

        self.session.stop()

        self.state.transition(

            VoiceState.STOPPED

        )

        self.publish(

            VoiceEventType.SYSTEM_STOPPED

        )

    # ---------------------------------------------------------

    def publish(

        self,

        event_type,

    ):

        event = VoiceEvent(

            event_type=event_type

        )

        self.logger.info(

            f"EVENT : {event.event_type.name}"

        )

    # ---------------------------------------------------------

    @property

    def current_state(self):

        return self.state.current

    # ---------------------------------------------------------

    @property

    def active_session(self):

        return self.session.active

    # ---------------------------------------------------------

    def health(self):

        return {

            "state": self.state.current.name,

            "session": self.session.active,

            "metrics": self.metrics.snapshot(),

        }