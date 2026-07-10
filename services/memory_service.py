from memory.memory import Memory


class MemoryService:

    """
    Business layer for Memory.

    Agents should communicate with this class
    instead of accessing Memory directly.
    """

    def __init__(self):

        self.memory = Memory()

    # =====================================================
    # Memory CRUD
    # =====================================================

    def remember(self, key, value, category="general"):

        self.memory.remember(
            key=key,
            value=value,
            category=category
        )

        return f"I'll remember your {key.replace('_', ' ')}."

    def recall(self, key):

        return self.memory.recall(key)

    def update(self, key, value, category="general"):

        self.memory.update(
            key=key,
            value=value,
            category=category
        )

        return f"I've updated your {key.replace('_', ' ')}."

    def forget(self, key):

        self.memory.forget(key)

        return f"I've forgotten your {key.replace('_', ' ')}."

    # =====================================================
    # Search
    # =====================================================

    def search(self, keyword):

        return self.memory.search(keyword)

    def list_all(self):

        return self.memory.list_all()

    def count(self):

        return self.memory.count()

    # =====================================================
    # Chat History
    # =====================================================

    def save_chat(self, user_message, assistant_message):

        self.memory.save_chat(
            user_message,
            assistant_message
        )

    def recent_chat(self, limit=10):

        return self.memory.recent_chat(limit)

    # =====================================================
    # Utilities
    # =====================================================

    def clear_memory(self):

        self.memory.clear_memory()

        return "All memories have been cleared."

    def has_memory(self, key):

        return self.memory.has_memory(key)