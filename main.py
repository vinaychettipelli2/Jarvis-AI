from ui.console import start_console
from ui.voice_console import start_voice_console


def main():

    print("\n========== JARVIS ==========")
    print("1. Text Mode")
    print("2. Voice Mode")
    print("3. Exit")

    choice = input("\nSelect: ")

    if choice == "1":
        start_console()

    elif choice == "2":
        start_voice_console()

    else:
        print("Goodbye.")


if __name__ == "__main__":
    main()