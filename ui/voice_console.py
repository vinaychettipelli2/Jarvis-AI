from engine.conversation_engine import ConversationEngine
from voice.voice_assistant import VoiceAssistant


def start_voice_console():

    engine = ConversationEngine()
    voice = VoiceAssistant()

    voice.greet()

    while True:

        question = input("\n🎤 You: ")

        if question.lower() in ("exit", "quit"):

            voice.speak("Goodbye Vinay.")
            break

        answer = engine.ask(question)

        print(f"\nJarvis: {answer}\n")

        voice.speak(answer)