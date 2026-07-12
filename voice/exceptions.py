"""
voice/exceptions.py

Centralized exceptions for the Voice module.
"""


class VoiceException(Exception):
    """
    Base exception for all voice-related errors.
    """

    default_message = "Voice module error."

    def __init__(self, message: str | None = None):
        super().__init__(message or self.default_message)


class ConfigurationError(VoiceException):
    default_message = "Invalid voice configuration."


class MicrophoneError(VoiceException):
    default_message = "Microphone initialization failed."


class RecordingError(VoiceException):
    default_message = "Audio recording failed."


class AudioFileError(VoiceException):
    default_message = "Audio file is invalid."


class SpeechRecognitionError(VoiceException):
    default_message = "Speech recognition failed."


class VoiceActivityError(VoiceException):
    default_message = "Voice activity detection failed."


class WakeWordError(VoiceException):
    default_message = "Wake word detection failed."


class SpeechSynthesisError(VoiceException):
    default_message = "Speech synthesis failed."


class AudioPlaybackError(VoiceException):
    default_message = "Audio playback failed."


class ConversationError(VoiceException):
    default_message = "Conversation engine failed."


class SessionTimeoutError(VoiceException):
    default_message = "Conversation session timed out."