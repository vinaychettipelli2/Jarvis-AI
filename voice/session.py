"""
voice/session.py

Production Conversation Session Manager.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from threading import RLock
from uuid import uuid4


@dataclass(slots=True)
class SessionMetadata:

    session_id: str = field(default_factory=lambda: str(uuid4()))

    started_at: datetime = field(default_factory=datetime.now)

    last_activity: datetime = field(default_factory=datetime.now)

    interaction_count: int = 0


class ConversationSession:
    """
    Thread-safe conversation session.
    """

    def __init__(self, timeout: int = 60):

        self._timeout = timeout

        self._lock = RLock()

        self._session: SessionMetadata | None = None

    @property
    def active(self) -> bool:

        with self._lock:

            return self._session is not None

    def start(self) -> SessionMetadata:

        with self._lock:

            self._session = SessionMetadata()

            return self._session

    def stop(self):

        with self._lock:

            self._session = None

    def touch(self):

        with self._lock:

            if self._session is None:
                return

            self._session.last_activity = datetime.now()

            self._session.interaction_count += 1

    def expired(self) -> bool:

        with self._lock:

            if self._session is None:
                return True

            return (

                datetime.now()

                >

                self._session.last_activity

                +

                timedelta(seconds=self._timeout)

            )

    @property
    def session_id(self):

        with self._lock:

            if self._session is None:
                return None

            return self._session.session_id

    @property
    def interactions(self):

        with self._lock:

            if self._session is None:
                return 0

            return self._session.interaction_count

    @property
    def started_at(self):

        with self._lock:

            if self._session is None:
                return None

            return self._session.started_at