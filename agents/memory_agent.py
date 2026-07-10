from services.memory_service import MemoryService
from core.ai_memory_detector import AIMemoryDetector


class MemoryAgent:
    """
    Memory Agent

    Responsibilities:
    - Save memory
    - Recall memory
    - Update memory
    - Forget memory
    - Search memory
    """

    def __init__(self):

        self.memory = MemoryService()
        self.detector = AIMemoryDetector()

    # =====================================================
    # Main Entry Point
    # =====================================================

    def execute(self, request):

        request = request.strip()

        lower = request.lower()

        # ==========================================
        # LIST ALL MEMORIES
        # ==========================================

        if "what do you know about me" in lower \
                or "show my memories" in lower \
                or "list my memories" in lower:

            memories = self.memory.list_all()

            if not memories:
                return "I don't know anything about you yet."

            lines = []

            for item in memories:

                key = item["memory_key"].replace("_", " ").title()

                value = item["memory_value"]

                lines.append(f"{key}: {value}")

            return "\n".join(lines)

        # ==========================================
        # MEMORY COUNT
        # ==========================================

        if "how many memories" in lower:

            return f"I currently have {self.memory.count()} memories."

        # ==========================================
        # FORGET MEMORY
        # ==========================================

        if lower.startswith("forget "):

            key = lower.replace("forget", "").strip()

            key = key.replace("my ", "")

            key = key.replace(" ", "_")

            return self.memory.forget(key)

        # ==========================================
        # SEARCH MEMORY
        # ==========================================

        if lower.startswith("search memory"):

            keyword = lower.replace("search memory", "").strip()

            results = self.memory.search(keyword)

            if not results:

                return "No matching memories found."

            output = []

            for item in results:

                output.append(
                    f"{item['memory_key']} = {item['memory_value']}"
                )

            return "\n".join(output)

        # ==========================================
        # AI MEMORY DETECTION
        # ==========================================

        detected = self.detector.detect(request)

        if detected.get("should_save"):

            return self.memory.remember(

                key=detected["key"],

                value=detected["value"],

                category=detected.get(
                    "category",
                    "general"
                )

            )

        # ==========================================
        # RECALL
        # ==========================================

        if "what is my" in lower or "who is my" in lower:

            key = lower

            key = key.replace("what is my", "")

            key = key.replace("who is my", "")

            key = key.replace("?", "")

            key = key.strip()

            key = key.replace(" ", "_")

            value = self.memory.recall(key)

            if value:

                return value

            return "I don't remember that yet."

        return None