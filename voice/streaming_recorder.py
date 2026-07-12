"""
voice/streaming_recorder.py

Enterprise Streaming Recorder
"""

from __future__ import annotations

from queue import Queue
from threading import Event, Lock
from typing import Optional

import numpy as np
import sounddevice as sd

from voice.interfaces import Recorder
from voice.exceptions import (
    RecordingError,
    MicrophoneError,
)
from voice.voice_logger import VoiceLogger


class StreamingRecorder(Recorder):
    """
    Enterprise Streaming Recorder.

    Features
    --------
    ✔ Continuous Recording
    ✔ Thread Safe
    ✔ Low Latency
    ✔ Queue Based
    ✔ Chunk Streaming
    ✔ Non Blocking
    ✔ Production Ready
    """

    def __init__(

        self,

        sample_rate: int = 16000,

        channels: int = 1,

        chunk_size: int = 1600,

        device: Optional[int] = None,

    ):

        self.logger = VoiceLogger.get_logger()

        self.sample_rate = sample_rate

        self.channels = channels

        self.chunk_size = chunk_size

        self.device = device

        self.queue: Queue[np.ndarray] = Queue()

        self.stop_event = Event()

        self.lock = Lock()

        self.stream = None

    # ---------------------------------------------------------

    def start(self):

        if self.stream:

            return

        self.logger.info(

            "Opening microphone stream."

        )

        self.stop_event.clear()

        self.stream = sd.InputStream(

            samplerate=self.sample_rate,

            channels=self.channels,

            blocksize=self.chunk_size,

            dtype="float32",

            callback=self._callback,

            device=self.device,

        )

        self.stream.start()

    # ---------------------------------------------------------

    def stop(self):

        with self.lock:

            if self.stream:

                self.stream.stop()

                self.stream.close()

                self.stream = None

                self.logger.info(

                    "Microphone stream closed."

                )

    # ---------------------------------------------------------

    def _callback(

        self,

        indata,

        frames,

        time,

        status,

    ):

        if status:

            self.logger.warning(

                str(status)

            )

        if self.stop_event.is_set():

            return

        self.queue.put(

            indata.copy()

        )

    # ---------------------------------------------------------

    def read(self):

        try:

            return self.queue.get(

                timeout=1

            )

        except Exception:

            return None

    # ---------------------------------------------------------

    def flush(self):

        while not self.queue.empty():

            self.queue.get_nowait()

    # ---------------------------------------------------------

    def available(self):

        return self.queue.qsize()

    # ---------------------------------------------------------

    @property

    def is_running(self):

        return self.stream is not None

    # ---------------------------------------------------------

    def record(self, duration=None):

        """
        Compatibility method.

        Streaming systems should use:

            start()
            read()
            stop()
        """

        raise RecordingError(

            "StreamingRecorder does not support record(). "
            "Use start()/read()/stop()."

        )