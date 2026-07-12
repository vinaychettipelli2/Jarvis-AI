# CHANGED: Replaced simpleaudio with sounddevice + soundfile for stable playback on Python 3.14.

"""
voice/audio_player.py

Production Audio Player
"""

from __future__ import annotations

from pathlib import Path
from threading import Lock, Thread
from typing import Optional

import numpy as np
import sounddevice as sd
import soundfile as sf

from voice.interfaces import AudioOutput
from voice.exceptions import (
    AudioPlaybackError,
    AudioFileError,
)
from voice.voice_logger import VoiceLogger


class AudioPlayer(AudioOutput):
    """
    Enterprise Audio Player

    Features
    --------
    ✔ Thread Safe
    ✔ Blocking Playback
    ✔ Non Blocking Playback
    ✔ Stop Playback
    ✔ Playback State
    ✔ Future Barge-In Ready
    ✔ Python 3.14 Compatible
    """

    def __init__(self):

        self.logger = VoiceLogger.get_logger()

        self._lock = Lock()

        self._playing = False

        self._thread: Optional[Thread] = None

        self._stream = None

    # ---------------------------------------------------------

    def play(
        self,
        audio: Path,
        blocking: bool = True,
    ) -> None:

        if not audio.exists():

            raise AudioFileError(
                f"Audio file not found: {audio}"
            )

        if blocking:

            self._play(audio)

        else:

            self._thread = Thread(
                target=self._play,
                args=(audio,),
                daemon=True,
                name="AudioPlayer",
            )

            self._thread.start()

    # ---------------------------------------------------------

    def _play(self, audio: Path):

        with self._lock:

            try:

                self._playing = True

                data, samplerate = sf.read(
                    str(audio),
                    dtype="float32",
                )

                self.logger.info(
                    f"Playing : {audio.name}"
                )

                sd.play(data, samplerate)

                sd.wait()

            except Exception as exc:

                self.logger.exception(exc)

                raise AudioPlaybackError(
                    str(exc)
                ) from exc

            finally:

                self._playing = False

    # ---------------------------------------------------------

    def stop(self):

        with self._lock:

            try:

                sd.stop()

            finally:

                self._playing = False

                self.logger.info(
                    "Playback stopped."
                )

    # ---------------------------------------------------------

    def wait(self):

        if self._thread:

            self._thread.join()

    # ---------------------------------------------------------

    @property
    def is_playing(self):

        return self._playing