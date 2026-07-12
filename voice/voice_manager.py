"""
voice/voice_manager.py

Enterprise Voice Manager
"""

from __future__ import annotations

from engine.conversation_engine import ConversationEngine

from voice.metrics import MetricsCollector
from voice.voice_assistant import VoiceAssistant
from voice.voice_logger import VoiceLogger
from voice.voice_state import VoiceState
from voice.worker import (
    RecordingWorker,
    TranscriptionWorker,
    AIWorker,
    SpeechWorker,
    PlaybackWorker,
)


class VoiceManager:
    """
    Enterprise Voice Manager.

    Responsibilities
    ----------------
    ✔ Voice orchestration
    ✔ AI interaction
    ✔ Worker lifecycle
    ✔ Metrics
    ✔ Graceful shutdown
    """

    EXIT_COMMANDS = {
        "exit",
        "quit",
        "bye",
        "goodbye",
        "shutdown",
        "stop",
    }

    def __init__(

        self,

        assistant: VoiceAssistant,

        engine: ConversationEngine,

        metrics: MetricsCollector,

    ):

        self.logger = VoiceLogger.get_logger()

        self.assistant = assistant

        self.engine = engine

        self.metrics = metrics

        self.running = False

        self.record_worker = RecordingWorker()

        self.stt_worker = TranscriptionWorker()

        self.ai_worker = AIWorker()

        self.tts_worker = SpeechWorker()

        self.play_worker = PlaybackWorker()

    # -----------------------------------------------------

    def start(self):

        self.logger.info(

            "Starting Voice Manager."

        )

        self.running = True

        self.assistant.initialize()

        self._start_workers()

        self.assistant.speak(

            "Hello Vinay. I am Jarvis."

        )

        while self.running:

            self._conversation_cycle()

    # -----------------------------------------------------

    def stop(self):

        self.running = False

        self.logger.info(

            "Stopping Voice Manager."

        )

        self._stop_workers()

        self.assistant.shutdown()

    # -----------------------------------------------------

    def _conversation_cycle(self):

        try:

            question = self.assistant.listen()

            if not question:

                return

            question = question.strip()

            if not question:

                return

            print(f"\n👤 You : {question}")

            if self._should_exit(question):

                self.assistant.speak(

                    "Goodbye Vinay."

                )

                self.stop()

                return

            self.assistant.state.transition(

                VoiceState.THINKING

            )

            with self.metrics.timer(

                "conversation"

            ):

                answer = self.engine.ask(

                    question

                )

            print(f"\n🤖 Jarvis : {answer}")

            self.assistant.speak(

                answer

            )

            self.assistant.state.transition(

                VoiceState.IDLE

            )

        except KeyboardInterrupt:

            self.stop()

        except Exception as exc:

            self.logger.exception(

                exc

            )

            self.metrics.increment(

                "errors"

            )

            try:

                self.assistant.speak(

                    "Sorry, something went wrong."

                )

            except Exception:

                pass

    # -----------------------------------------------------

    def _start_workers(self):

        self.record_worker.start()

        self.stt_worker.start()

        self.ai_worker.start()

        self.tts_worker.start()

        self.play_worker.start()

    # -----------------------------------------------------

    def _stop_workers(self):

        self.record_worker.stop()

        self.stt_worker.stop()

        self.ai_worker.stop()

        self.tts_worker.stop()

        self.play_worker.stop()

    # -----------------------------------------------------

    @classmethod

    def _should_exit(

        cls,

        text: str,

    ) -> bool:

        return text.lower() in cls.EXIT_COMMANDS

    # -----------------------------------------------------

    @property

    def health(self):

        return {

            "running": self.running,

            "workers": {

                "record": self.record_worker.thread.is_alive(),

                "stt": self.stt_worker.thread.is_alive(),

                "ai": self.ai_worker.thread.is_alive(),

                "tts": self.tts_worker.thread.is_alive(),

                "play": self.play_worker.thread.is_alive(),

            },

            "metrics": self.metrics.snapshot(),

        }