import os
import subprocess


class DesktopAgent:

    def __init__(self):
        """
        Desktop Agent

        Responsible for:
        - Open Applications
        - Launch Programs
        - Open Folders
        """

    def execute(self, question):

        question = question.lower()

        if "chrome" in question:
            return self.open_chrome()

        elif "vscode" in question or "vs code" in question:
            return self.open_vscode()

        elif "notepad" in question:
            return self.open_notepad()

        elif "calculator" in question:
            return self.open_calculator()

        elif "explorer" in question or "folder" in question:
            return self.open_explorer()

        return "Desktop command not recognized."

    def open_chrome(self):

        try:
            os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
            return "Opening Google Chrome..."
        except:
            return "Chrome not found."

    def open_vscode(self):

        try:
            os.startfile("C:\\Users\\Winay\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
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

        return "Opening File Explorer..."