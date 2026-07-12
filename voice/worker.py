"""
voice/worker.py

Enterprise Background Worker Framework
"""

from __future__ import annotations

from threading import Thread, Event
from queue import Queue, Empty
from typing import Callable, Any
from dataclasses import dataclass
import traceback

from voice.voice_logger import VoiceLogger


@dataclass(slots=True)
class WorkerTask:

    name: str

    callback: Callable[..., Any]

    args: tuple = ()

    kwargs: dict | None = None


class BackgroundWorker:
    """
    Enterprise Background Worker

    Features
    --------
    ✔ Thread Safe
    ✔ Queue Based
    ✔ Graceful Shutdown
    ✔ Exception Isolation
    ✔ Production Logging
    """

    def __init__(

        self,

        name: str,

    ):

        self.logger = VoiceLogger.get_logger()

        self.name = name

        self.queue: Queue[WorkerTask] = Queue()

        self.stop_event = Event()

        self.thread = Thread(

            target=self._run,

            name=name,

            daemon=True,

        )

    # ---------------------------------------------------------

    def start(self):

        if not self.thread.is_alive():

            self.logger.info(

                f"{self.name} started."

            )

            self.thread.start()

    # ---------------------------------------------------------

    def submit(

        self,

        task: WorkerTask,

    ):

        self.queue.put(task)

    # ---------------------------------------------------------

    def stop(self):

        self.stop_event.set()

        self.thread.join(timeout=3)

        self.logger.info(

            f"{self.name} stopped."

        )

    # ---------------------------------------------------------

    def _run(self):

        while not self.stop_event.is_set():

            try:

                task = self.queue.get(

                    timeout=0.25

                )

            except Empty:

                continue

            try:

                kwargs = task.kwargs or {}

                task.callback(

                    *task.args,

                    **kwargs,

                )

            except Exception:

                self.logger.error(

                    traceback.format_exc()

                )

            finally:

                self.queue.task_done()


# ==========================================================
# Specialized Workers
# ==========================================================

class RecordingWorker(BackgroundWorker):

    def __init__(self):

        super().__init__(

            "RecordingWorker"

        )


class TranscriptionWorker(BackgroundWorker):

    def __init__(self):

        super().__init__(

            "TranscriptionWorker"

        )


class AIWorker(BackgroundWorker):

    def __init__(self):

        super().__init__(

            "AIWorker"

        )


class SpeechWorker(BackgroundWorker):

    def __init__(self):

        super().__init__(

            "SpeechWorker"

        )


class PlaybackWorker(BackgroundWorker):

    def __init__(self):

        super().__init__(

            "PlaybackWorker"

        )