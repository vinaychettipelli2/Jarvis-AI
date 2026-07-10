from engine.conversation_engine import ConversationEngine


class ConsoleUI:

    def __init__(self):

        self.engine = ConversationEngine()

    def banner(self):

        print("=" * 45)
        print("            JARVIS AI")
        print("=" * 45)

        print()
        print("Hello Vinay!")
        print("I'm online.")
        print("Type 'exit' to quit.")
        print()

    def start(self):

        self.banner()

        while True:

            try:

                question = input("You : ").strip()

                if question == "":
                    continue

                if question.lower() in [
                    "exit",
                    "quit"
                ]:

                    print()
                    print("Jarvis : Goodbye Vinay! 👋")
                    break

                answer = self.engine.process(question)

                print()
                print("Jarvis :", answer)
                print()

            except KeyboardInterrupt:

                print()
                print("Jarvis : Goodbye Vinay! 👋")
                break

            except Exception as e:

                print()
                print("Jarvis Error :", e)
                print()


def start_console():

    ui = ConsoleUI()

    ui.start()