class SafetyAgent:

    def __init__(self):
        """
        Safety Agent

        Responsible for:

        - Dangerous Commands
        - Confirmation
        - Permission Checking
        """

        self.blocked_words = [
            "delete",
            "format",
            "shutdown",
            "remove",
            "erase"
        ]

    def execute(self, question):

        question = question.lower()

        for word in self.blocked_words:

            if word in question:
                return (
                    "⚠ Dangerous command detected.\n"
                    "Confirmation required."
                )

        return "Command is safe."

    def is_safe(self, question):

        question = question.lower()

        for word in self.blocked_words:

            if word in question:
                return False

        return True