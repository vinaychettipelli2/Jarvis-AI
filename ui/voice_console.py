"""
ui/voice_console.py

Enterprise Voice Composition Root
"""

from engine.conversation_engine import ConversationEngine

from voice.audio_pipeline import AudioPipeline
from voice.audio_player import AudioPlayer
from voice.calibration import MicrophoneCalibrator
from voice.metrics import MetricsCollector
from voice.microphone import MicrophoneManager
from voice.openwakeword_detector import OpenWakeWordDetector
from voice.session import ConversationSession
from voice.speech_to_text import SpeechToText
from voice.text_to_speech import TextToSpeech
from voice.voice_assistant import VoiceAssistant
from voice.voice_config import VoiceConfig
from voice.voice_manager import VoiceManager
from voice.webrtc_vad import WebRTCVAD


def start_voice_console():

    # ----------------------------------------------------
    # Configuration
    # ----------------------------------------------------

    config = VoiceConfig()

    metrics = MetricsCollector()

    session = ConversationSession(

        timeout=config.conversation_timeout

    )

    # ----------------------------------------------------
    # Audio
    # ----------------------------------------------------

    recorder = MicrophoneManager(

        sample_rate=config.sample_rate,

        channels=config.channels,

        device=config.microphone_index,

    )

    calibrator = MicrophoneCalibrator(

        sample_rate=config.sample_rate,

        channels=config.channels,

        device=config.microphone_index,

    )

    vad = WebRTCVAD(

        aggressiveness=2,

        sample_rate=config.sample_rate,

    )

    wakeword = OpenWakeWordDetector(

        model_path="models/wakeword/jarvis.onnx",

        wake_word=config.wake_word,

        threshold=0.50,

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

    # ----------------------------------------------------
    # Pipeline
    # ----------------------------------------------------

    pipeline = AudioPipeline(

        recorder=recorder,

        recognizer=recognizer,

        vad=vad,

        wake_word=wakeword,

        calibrator=calibrator,

        metrics=metrics,

        session=session,

    )

    # ----------------------------------------------------
    # Voice Assistant
    # ----------------------------------------------------

    assistant = VoiceAssistant(

        pipeline=pipeline,

        synthesizer=synthesizer,

        player=player,

        session=session,

        metrics=metrics,

    )

    # ----------------------------------------------------
    # AI
    # ----------------------------------------------------

    engine = ConversationEngine()

    # ----------------------------------------------------
    # Voice Manager
    # ----------------------------------------------------

    manager = VoiceManager(

        assistant=assistant,

        engine=engine,

        metrics=metrics,

    )

    # ----------------------------------------------------

    manager.start()