"""
voice/voice_config.py

Production Configuration Loader
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import yaml

from voice.exceptions import ConfigurationError


@dataclass(slots=True, frozen=True)
class VoiceConfiguration:

    enabled: bool

    wake_word: str

    sample_rate: int

    channels: int

    microphone_index: int | None

    speaker_index: int | None

    whisper_model: str

    whisper_device: str

    whisper_compute_type: str

    whisper_language: str

    whisper_beam_size: int

    piper_path: str

    voice_model: str

    output_file: str

    conversation_timeout: int


class VoiceConfig:

    def __init__(self, config_file: str = "config/config.yml"):

        path = Path(config_file)

        if not path.exists():

            raise ConfigurationError(

                f"Configuration file not found: {path}"

            )

        with open(path, "r", encoding="utf-8") as file:

            cfg = yaml.safe_load(file)

        voice = cfg.get("voice", {})

        stt = cfg.get("speech_to_text", {})

        tts = cfg.get("text_to_speech", {})

        self.config = VoiceConfiguration(

            enabled=voice.get("enabled", True),

            wake_word=voice.get("wake_word", "jarvis").lower(),

            sample_rate=int(

                voice.get("sample_rate", 16000)

            ),

            channels=int(

                voice.get("channels", 1)

            ),

            microphone_index=voice.get(

                "microphone_index"

            ),

            speaker_index=voice.get(

                "speaker_index"

            ),

            whisper_model=stt.get(

                "model",

                "models/whisper"

            ),

            whisper_device=stt.get(

                "device",

                "cpu"

            ),

            whisper_compute_type=stt.get(

                "compute_type",

                "int8"

            ),

            whisper_language=stt.get(

                "language",

                "en"

            ),

            whisper_beam_size=int(

                stt.get("beam_size", 5)

            ),

            piper_path=tts.get(

                "piper_path"

            ),

            voice_model=tts.get(

                "voice"

            ),

            output_file=tts.get(

                "output",

                "jarvis_output.wav"

            ),

            conversation_timeout=int(

                voice.get(

                    "conversation_timeout",

                    30

                )

            )

        )

    def __getattr__(self, item):

        return getattr(self.config, item)

    def as_dict(self):

        return self.config.__dict__.copy()