import re


class IntentDetector:

    """
    Detects the user's intent and tells the planner
    which agent should handle the request.
    """

    def __init__(self):

        self.intents = {

            "memory": [
                r"my name is",
                r"my favourite bike is",
                r"my favorite bike is",
                r"my manager is",
                r"i work at",
                r"i work for",
                r"i am from",
                r"i live in",
                r"my age is",
                r"my email is",
                r"my phone number is",
                r"remember"
            ],

            "research": [
                r"latest",
                r"news",
                r"research",
                r"search",
                r"documentation",
                r"weather",
                r"today",
                r"current",
                r"who is",
                r"what happened"
            ],

            "desktop": [
                r"open",
                r"launch",
                r"start",
                r"run",
                r"close"
            ],

            "trading": [
                r"bitcoin",
                r"btc",
                r"ethereum",
                r"eth",
                r"crypto",
                r"stock",
                r"market",
                r"price"
            ],

            "voice": [
                r"speak",
                r"listen",
                r"voice"
            ],

            "safety": [
                r"delete",
                r"erase",
                r"shutdown",
                r"format"
            ]
        }

    def detect(self, question):

        question = question.lower().strip()

        # Memory Recall
        if (
            "what is my" in question
            or "who is my" in question
            or "where do i work" in question
        ):
            return "memory"

        # Memory Save
        for pattern in self.intents["memory"]:

            if re.search(pattern, question):
                return "memory"

        # Research
        for pattern in self.intents["research"]:

            if re.search(pattern, question):
                return "research"

        # Desktop
        for pattern in self.intents["desktop"]:

            if re.search(pattern, question):
                return "desktop"

        # Trading
        for pattern in self.intents["trading"]:

            if re.search(pattern, question):
                return "trading"

        # Voice
        for pattern in self.intents["voice"]:

            if re.search(pattern, question):
                return "voice"

        # Safety
        for pattern in self.intents["safety"]:

            if re.search(pattern, question):
                return "safety"

        # Default
        return "ai"

    def is_ai(self, question):

        return self.detect(question) == "ai"

    def is_memory(self, question):

        return self.detect(question) == "memory"

    def is_research(self, question):

        return self.detect(question) == "research"

    def is_desktop(self, question):

        return self.detect(question) == "desktop"

    def is_trading(self, question):

        return self.detect(question) == "trading"

    def is_voice(self, question):

        return self.detect(question) == "voice"

    def is_safe(self, question):

        return self.detect(question) != "safety"