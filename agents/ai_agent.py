from services.ai_service import AIService


class AIAgent:

    def __init__(self):
        self.ai = AIService()

    def execute(self, question, history=None):
        """
        Executes an AI conversation using the Ollama model.

        Parameters
        ----------
        question : str
            User's current question.

        history : list
            Previous conversation history.

        Returns
        -------
        str
            AI response.
        """

        if history is None:
            history = []

        messages = []

        # Add previous conversation
        messages.extend(history)

        # Add current user question
        messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        # Ask Ollama
        response = self.ai.ask(messages)

        return response