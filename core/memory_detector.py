import json

from services.ai_service import AIService


class AIMemoryDetector:

    def __init__(self):

        self.ai = AIService()

    def detect(self, user_message):

        prompt = f"""
You are Jarvis Memory.

Your job is to determine whether the user's message contains
long-term information worth remembering.

Examples of things to remember:

- Name
- Age
- Birthday
- Company
- Manager
- Profession
- Address
- City
- Country
- Favorite things
- Bike
- Car
- Laptop
- Phone
- Skills
- Education
- Goals
- Projects
- Personal preferences

Do NOT remember:

- Greetings
- Questions
- Temporary events
- Commands
- Small talk

Return ONLY valid JSON.

Example:

{{
    "should_save": true,
    "key": "favorite_bike",
    "value": "KTM Duke 200",
    "category": "preferences"
}}

If nothing should be saved:

{{
    "should_save": false
}}

User:

{user_message}
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

            start = response.find("{")

            end = response.rfind("}") + 1

            response = response[start:end]

            return json.loads(response)

        except Exception:

            return {

                "should_save": False

            }   