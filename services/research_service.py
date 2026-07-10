from services.research.duckduckgo_provider import DuckDuckGoProvider
from services.ai_service import AIService


class ResearchService:

    def __init__(self):

        self.provider = DuckDuckGoProvider()
        self.ai = AIService()

    # ==========================================
    # General Search
    # ==========================================

    def search(self, query):

        results = self.provider.search(query)

        return self.summarize(
            query,
            results
        )

    # ==========================================
    # News Search
    # ==========================================

    def latest_news(self, topic):

        results = self.provider.news(topic)

        return self.summarize(
            topic,
            results
        )

    # ==========================================
    # AI Summary
    # ==========================================

    def summarize(self, query, results):

        if not results:

            return "No results found."

        text = ""

        for index, item in enumerate(results, start=1):

            title = item.get("title", "")

            body = item.get("body", "")

            href = (
                item.get("href")
                or item.get("url")
                or ""
            )

            text += f"""
Result {index}

Title:
{title}

Description:
{body}

Link:
{href}

"""

        prompt = f"""
You are Jarvis.

The user searched:

{query}

Below are the live search results.

{text}

Summarize the results.

Provide:

1. Key points
2. Important facts
3. Short summary

Do not invent information.
"""

        messages = [

            {
                "role": "user",
                "content": prompt
            }

        ]

        return self.ai.ask(messages)