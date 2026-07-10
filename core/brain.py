from services.ai_service import AIService
from services.memory_service import MemoryService


class Brain:

    def __init__(self):
        self.ai = AIService()
        self.memory = MemoryService()

    def ask(self, question):

        question_lower = question.lower().strip()

        # Answer from memory
        if question_lower == "what is my name?":
            name = self.memory.recall("name")

            if name:
                return f"Your name is {name.title()}."

            return "I don't know your name yet."

        if question_lower == "what is my favorite bike?":
            bike = self.memory.recall("favorite_bike")

            if bike:
                return f"Your favorite bike is {bike}."

            return "I don't know your favorite bike yet."

        # Otherwise use AI
        return self.ai.ask(question)