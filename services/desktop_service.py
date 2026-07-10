import os
import subprocess


class DesktopService:

    def open_chrome(self):

        try:

            os.startfile(
                r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            )

            return "Opening Chrome..."

        except:

            return "Chrome not found."

    def open_vscode(self):

        try:

            os.startfile(
                r"C:\Users\Winay\AppData\Local\Programs\Microsoft VS Code\Code.exe"
            )

            return "Opening VS Code..."

        except:

            return "VS Code not found."

    def open_notepad(self):

        subprocess.Popen("notepad.exe")

        return "Opening Notepad..."

    def open_calculator(self):

        subprocess.Popen("calc.exe")

        return "Opening Calculator..."

    def open_explorer(self):

        subprocess.Popen("explorer.exe")

        return "Opening Explorer..."