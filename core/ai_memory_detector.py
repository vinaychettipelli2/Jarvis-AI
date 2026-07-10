import json
import re

from services.ai_service import AIService


class AIMemoryDetector:
    """
    AI-powered memory detector.

    Responsibilities:
    - Decide if something should be remembered.
    - Extract structured memory.
    - Return valid JSON.
    """

    def __init__(self):

        self.ai = AIService()

    def detect(self, message):

        prompt = f"""
You are Jarvis Memory.

Analyze the user's message.

Your task is to decide whether the message contains useful LONG-TERM information
that would help you become a better personal assistant.

Examples of things worth remembering:

• Personal information
• Preferences
• Favorite things
• Career
• Skills
• Devices
• Projects
• Goals
• Education
• Relationships
• Important long-term facts

Do NOT remember:

• Greetings
• Temporary events
• Questions
• Commands
• General conversation
• One-time activities

If the message should NOT be remembered return ONLY:

{{
    "should_save": false
}}

Otherwise return ONLY valid JSON.

Example:

{{
    "should_save": true,
    "key": "favorite_bike",
    "value": "KTM Duke 200",
    "category": "preferences",
    "importance": 9
}}

Rules:

1. Return ONLY JSON.
2. No explanation.
3. No markdown.
4. importance = 1-10
5. key should use snake_case.

User message:

{message}
"""

        try:

            response = self.ai.ask(
                [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract JSON safely
            match = re.search(r"\{.*\}", response, re.DOTALL)

            if not match:
                return {
                    "should_save": False
                }

            return json.loads(match.group())

        except Exception:

            return {
                "should_save": False
            }