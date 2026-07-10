from core.brain import Brain


def start_console():

    brain = Brain()

    print("=" * 34)
    print("          JARVIS AI")
    print("=" * 34)

    print()
    print("Hello Vinay!")
    print("I'm online.")
    print("Type 'exit' to quit.")
    print()

    while True:

        question = input("You: ")

        if question.lower() in ["exit", "quit"]:

            print("\nJarvis: Goodbye Vinay! 👋")
            break

        answer = brain.ask(question)

        print("\nJarvis:", answer)
        print()