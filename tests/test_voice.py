"""
tests/test_voice.py

Production Integration Test
"""

from __future__ import annotations

import traceback

from engine.conversation_engine import ConversationEngine

from voice.audio_player import AudioPlayer
from voice.microphone import MicrophoneManager
from voice.session import ConversationSession
from voice.speech_to_text import SpeechToText
from voice.text_to_speech import TextToSpeech
from voice.vad import EnergyBasedVAD
from voice.voice_assistant import VoiceAssistant
from voice.voice_config import VoiceConfig
from voice.voice_manager import VoiceManager


def main():

    print("=" * 70)
    print("JARVIS Voice Module Integration Test")
    print("=" * 70)

    try:

        config = VoiceConfig()

        recorder = MicrophoneManager(

            sample_rate=config.sample_rate,

            channels=config.channels,

            device=config.microphone_index,

        )

        recognizer = SpeechToText(

            model_path=config.whisper_model,

            device=config.whisper_device,

            compute_type=config.whisper_compute_type,

            language=config.whisper_language,

            beam_size=config.whisper_beam_size,

        )

        synthesizer = TextToSpeech(

            piper_path=config.piper_path,

            voice_path=config.voice_model,

            output_file=config.output_file,

        )

        player = AudioPlayer()

        vad = EnergyBasedVAD()

        session = ConversationSession(

            timeout=config.conversation_timeout,

        )

        assistant = VoiceAssistant(

            recorder=recorder,

            recognizer=recognizer,

            synthesizer=synthesizer,

            player=player,

            vad=vad,

            session=session,

        )

        engine = ConversationEngine()

        manager = VoiceManager(

            assistant=assistant,

            engine=engine,

        )

        print()

        print("✓ Configuration Loaded")

        print("✓ Microphone Initialized")

        print("✓ Whisper Loaded")

        print("✓ Piper Loaded")

        print("✓ Voice Assistant Ready")

        print("✓ Conversation Engine Ready")

        print()

        manager.start()

    except Exception:

        traceback.print_exc()


if __name__ == "__main__":

    main()