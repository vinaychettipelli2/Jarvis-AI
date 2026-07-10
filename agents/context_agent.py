class ContextAgent:

    def __init__(self):
        """
        Stores the current conversation.
        Only the last N messages are kept.
        """

        self.history = []
        self.max_history = 10

    def add(self, role, message):
        """
        Add a message to conversation history.
        """

        self.history.append(
            {
                "role": role,
                "content": message
            }
        )

        # Keep only recent messages
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_history(self):
        """
        Return conversation history.
        """

        return self.history.copy()

    def clear(self):
        """
        Clear current conversation.
        """

        self.history.clear()

    def last_message(self):
        """
        Return last conversation message.
        """

        if self.history:
            return self.history[-1]

        return None

    def message_count(self):
        """
        Number of messages stored.
        """

        return len(self.history)

    def print_history(self):
        """
        Debug helper.
        """

        for message in self.history:
            print(
                f"{message['role']} : {message['content']}"
            )