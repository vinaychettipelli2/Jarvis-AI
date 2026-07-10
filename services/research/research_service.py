from services.research.duckduckgo_provider import DuckDuckGoProvider
from services.research.news_provider import NewsProvider
from services.research.weather_provider import WeatherProvider
from services.research.crypto_provider import CryptoProvider

from services.ai_service import AIService


class ResearchService:

    """
    Central Research Service.

    Responsible for selecting the correct
    provider based on the user's request.
    """

    def __init__(self):

        self.search_provider = DuckDuckGoProvider()

        self.news_provider = NewsProvider()

        self.weather_provider = WeatherProvider()

        self.crypto_provider = CryptoProvider()

        self.ai = AIService()

    # =====================================================

    def research(self, question):

        question_lower = question.lower()

        # ----------------------------
        # Weather
        # ----------------------------

        if "weather" in question_lower:

            city = question_lower.replace(
                "weather",
                ""
            ).replace(
                "in",
                ""
            ).strip()

            if city == "":
                city = "Hyderabad"

            return self.weather_provider.get_weather(
                city
            )

        # ----------------------------
        # Crypto
        # ----------------------------

        crypto_map = {

            "bitcoin": "bitcoin",

            "btc": "bitcoin",

            "ethereum": "ethereum",

            "eth": "ethereum",

            "solana": "solana",

            "dogecoin": "dogecoin",

            "doge": "dogecoin",

            "xrp": "ripple"

        }

        for key, coin in crypto_map.items():

            if key in question_lower:

                return self.crypto_provider.get_price(
                    coin
                )

        # ----------------------------
        # News
        # ----------------------------

        if "news" in question_lower or "latest" in question_lower:

            topic = question_lower

            topic = topic.replace(
                "latest",
                ""
            )

            topic = topic.replace(
                "news",
                ""
            ).strip()

            if topic == "":
                topic = "technology"

            return self.news_provider.search(
                topic
            )

        # ----------------------------
        # General Search
        # ----------------------------

        return self.search_provider.search(
            question
        )

    # =====================================================

    def summarize(self, question):

        result = self.research(question)

        if not result.get("success"):

            return result

        prompt = f"""
You are Jarvis.

The user asked:

{question}

Research Result:

{result}

Provide:

1. Short answer

2. Important facts

3. Professional summary

Keep the answer concise.
"""

        answer = self.ai.ask(

            [

                {

                    "role": "user",

                    "content": prompt

                }

            ]

        )

        return {

            "success": True,

            "type": "research",

            "message": answer,

            "data": result

        }