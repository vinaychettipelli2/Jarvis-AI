"""
voice/events.py

Enterprise Event System
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from uuid import uuid4


class VoiceEventType(Enum):

    SYSTEM_STARTED = auto()

    SYSTEM_STOPPED = auto()

    MICROPHONE_OPENED = auto()

    MICROPHONE_CLOSED = auto()

    RECORDING_STARTED = auto()

    RECORDING_STOPPED = auto()

    WAKE_WORD_DETECTED = auto()

    SPEECH_DETECTED = auto()

    SILENCE_DETECTED = auto()

    TRANSCRIPTION_STARTED = auto()

    TRANSCRIPTION_FINISHED = auto()

    AI_REQUEST_STARTED = auto()

    AI_REQUEST_FINISHED = auto()

    TTS_STARTED = auto()

    TTS_FINISHED = auto()

    PLAYBACK_STARTED = auto()

    PLAYBACK_FINISHED = auto()

    ERROR = auto()


@dataclass(slots=True, frozen=True)
class VoiceEvent:

    event_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    event_type: VoiceEventType = VoiceEventType.SYSTEM_STARTED

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )

    payload: dict = field(
        default_factory=dict
    )