"""
voice/voice_state.py

Production Voice State Management.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from threading import Lock
from datetime import datetime


class VoiceState(Enum):
    """
    Voice engine lifecycle.
    """

    INITIALIZING = auto()

    IDLE = auto()

    WAITING_WAKE_WORD = auto()

    LISTENING = auto()

    RECORDING = auto()

    TRANSCRIBING = auto()

    THINKING = auto()

    SPEAKING = auto()

    STOPPING = auto()

    STOPPED = auto()

    ERROR = auto()


@dataclass(slots=True)
class StateSnapshot:

    state: VoiceState

    previous_state: VoiceState | None

    changed_at: datetime


class VoiceStateManager:
    """
    Thread-safe Voice State Manager.
    """

    def __init__(self):

        self._lock = Lock()

        self._current = VoiceState.INITIALIZING

        self._previous = None

        self._changed_at = datetime.now()

    @property
    def current(self) -> VoiceState:

        with self._lock:
            return self._current

    @property
    def previous(self) -> VoiceState | None:

        with self._lock:
            return self._previous

    def transition(self, state: VoiceState) -> None:

        with self._lock:

            if self._current == state:
                return

            self._previous = self._current

            self._current = state

            self._changed_at = datetime.now()

    def snapshot(self) -> StateSnapshot:

        with self._lock:

            return StateSnapshot(

                state=self._current,

                previous_state=self._previous,

                changed_at=self._changed_at,

            )

    def is_idle(self):

        return self.current == VoiceState.IDLE

    def is_listening(self):

        return self.current == VoiceState.LISTENING

    def is_speaking(self):

        return self.current == VoiceState.SPEAKING

    def is_transcribing(self):

        return self.current == VoiceState.TRANSCRIBING

    def is_thinking(self):

        return self.current == VoiceState.THINKING

    def reset(self):

        self.transition(
            VoiceState.IDLE
        )