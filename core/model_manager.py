"""
JARVIS Model Manager

Central place for loading and managing all AI models.

Future supported models:
- Ollama
- Faster Whisper
- Piper
- Embedding Models

This avoids every module downloading/loading models independently.
"""

from pathlib import Path
import logging

logger = logging.getLogger("jarvis.model")


class ModelManager:

    def __init__(self):

        self.models_directory = Path("models")

        self.models_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def ensure_directory(self):

        """
        Creates model directory if missing.
        """

        self.models_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def model_exists(self, relative_path: str) -> bool:

        return (self.models_directory / relative_path).exists()

    def get_model_path(self, relative_path: str):

        return self.models_directory / relative_path

    def list_models(self):

        if not self.models_directory.exists():
            return []

        return [
            p.name
            for p in self.models_directory.iterdir()
            if p.is_dir()
        ]