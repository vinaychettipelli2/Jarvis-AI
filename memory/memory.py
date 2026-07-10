from memory.database import Database


class Memory:

    def __init__(self):
        self.db = Database()

    def remember(self, key, value):
        self.db.save_memory(key, value)

    def recall(self, key):
        return self.db.get_memory(key)

    def save_chat(self, user_message, jarvis_response):
        self.db.save_conversation(user_message, jarvis_response)