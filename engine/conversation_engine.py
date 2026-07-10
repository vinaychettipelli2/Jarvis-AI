from engine.planner import Planner
from engine.agent_manager import AgentManager


class ConversationEngine:

    def __init__(self):
        """
        Conversation Engine

        Main controller of Jarvis.
        """

        self.planner = Planner()
        self.manager = AgentManager()

    def process(self, question):

        if question is None:
            return "Please enter a question."

        question = question.strip()

        if len(question) == 0:
            return "Please enter a question."

        # Ask planner which agent should handle it
        selected_agent = self.planner.plan(question)

        # Execute selected agent
        answer = self.manager.execute(
            selected_agent,
            question
        )

        return answer

    def chat(self, question):

        return self.process(question)

    def ask(self, question):

        return self.process(question)

    def run(self):

        print("=" * 40)
        print("          JARVIS AI")
        print("=" * 40)

        print()
        print("Hello Vinay!")
        print("I'm online.")
        print("Type 'exit' to quit.")
        print()

        while True:

            question = input("You : ")

            if question.lower() in [
                "exit",
                "quit"
            ]:

                print("\nJarvis : Goodbye Vinay! 👋")
                break

            answer = self.process(question)

            print()

            print("Jarvis :", answer)

            print()