"""
voice/audio_player.py

Production Audio Player
"""

from __future__ import annotations

from pathlib import Path
from threading import Lock
from typing import Optional

import simpleaudio as sa

from voice.interfaces import AudioOutput
from voice.exceptions import (
    AudioPlaybackError,
    AudioFileError,
)
from voice.voice_logger import VoiceLogger


class AudioPlayer(AudioOutput):
    """
    Enterprise Audio Player.

    Features
    --------
    ✔ Thread Safe
    ✔ Blocking / Non-blocking playback
    ✔ Stop playback
    ✔ Playback status
    ✔ Production Logging
    """

    def __init__(self):

        self.logger = VoiceLogger.get_logger()

        self._lock = Lock()

        self._play_object: Optional[sa.PlayObject] = None

    # ---------------------------------------------------------

    def play(
        self,
        audio: Path,
        blocking: bool = True,
    ) -> None:

        with self._lock:

            try:

                if not audio.exists():

                    raise AudioFileError(

                        f"File not found : {audio}"

                    )

                wave = sa.WaveObject.from_wave_file(

                    str(audio)

                )

                self._play_object = wave.play()

                self.logger.info(

                    f"Playing : {audio.name}"

                )

                if blocking:

                    self._play_object.wait_done()

            except Exception as exc:

                raise AudioPlaybackError(

                    str(exc)

                ) from exc

    # ---------------------------------------------------------

    def stop(self):

        with self._lock:

            if self._play_object:

                self._play_object.stop()

                self.logger.info(

                    "Playback stopped."

                )

    # ---------------------------------------------------------

    @property
    def is_playing(self) -> bool:

        with self._lock:

            if self._play_object is None:
                return False

            return self._play_object.is_playing()

    # ---------------------------------------------------------

    def wait(self):

        with self._lock:

            if self._play_object:

                self._play_object.wait_done()