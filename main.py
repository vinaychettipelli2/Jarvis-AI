"""
main.py

JARVIS AI
Application Entry Point
"""

from __future__ import annotations

import sys

from ui.console import start_console
from ui.voice_console import start_voice_console


class JarvisApplication:
    """
    JARVIS Application Bootstrapper.

    Responsibilities
    ----------------
    ✔ Application Startup
    ✔ Mode Selection
    ✔ Graceful Shutdown
    ✔ Exception Handling
    """

    def run(self):

        while True:

            try:

                self._print_banner()

                choice = input("\nSelect : ").strip()

                if choice == "1":

                    start_console()

                elif choice == "2":

                    start_voice_console()

                elif choice == "3":

                    self.shutdown()

                    return

                else:

                    print("\nInvalid Option.\n")

            except KeyboardInterrupt:

                print("\n")

                self.shutdown()

                return

            except Exception as exc:

                print(f"\nApplication Error : {exc}\n")

    # ---------------------------------------------------------

    @staticmethod
    def _print_banner():

        print()

        print("=" * 50)

        print("             JARVIS AI")

        print("=" * 50)

        print()

        print("1. Text Mode")

        print("2. Voice Mode")

        print("3. Exit")

    # ---------------------------------------------------------

    @staticmethod
    def shutdown():

        print("\nShutting down Jarvis...\n")

        print("Goodbye Vinay!\n")

        sys.exit(0)


def main():

    app = JarvisApplication()

    app.run()


if __name__ == "__main__":

    main()