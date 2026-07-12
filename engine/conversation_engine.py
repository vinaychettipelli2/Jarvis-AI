"""
engine/conversation_engine.py

Production Conversation Engine
"""

from __future__ import annotations

from typing import Optional

from engine.agent_manager import AgentManager
from engine.planner import Planner


class ConversationEngine:
    """
    Enterprise Conversation Engine.

    Responsibilities
    ----------------
    ✔ Validate input
    ✔ Select agent
    ✔ Execute request
    ✔ Return response

    This class NEVER:
    - Talks to microphone
    - Performs TTS
    - Performs STT
    - Handles UI
    """

    def __init__(
        self,
        planner: Optional[Planner] = None,
        manager: Optional[AgentManager] = None,
    ):

        self.planner = planner or Planner()

        self.manager = manager or AgentManager()

    # ---------------------------------------------------------

    def ask(
        self,
        question: str,
    ) -> str:

        question = self._normalize(question)

        agent = self.planner.plan(question)

        return self.manager.execute(

            agent,

            question,

        )

    # ---------------------------------------------------------

    def chat(
        self,
        question: str,
    ) -> str:

        return self.ask(question)

    # ---------------------------------------------------------

    def process(
        self,
        question: str,
    ) -> str:

        return self.ask(question)

    # ---------------------------------------------------------

    @staticmethod
    def _normalize(
        question: str,
    ) -> str:

        if question is None:

            raise ValueError(

                "Question cannot be None."

            )

        question = question.strip()

        if not question:

            raise ValueError(

                "Question cannot be empty."

            )

        return question

    # ---------------------------------------------------------

    def health(self) -> dict:

        return {

            "planner": self.planner.__class__.__name__,

            "agent_manager": self.manager.__class__.__name__,

            "status": "healthy",

        }

    # ---------------------------------------------------------

    def __repr__(self):

        return (

            f"{self.__class__.__name__}"

            "("

            f"planner={self.planner.__class__.__name__}, "

            f"manager={self.manager.__class__.__name__}"

            ")"

        )