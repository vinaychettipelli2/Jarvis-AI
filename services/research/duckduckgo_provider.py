from duckduckgo_search import DDGS


class DuckDuckGoProvider:

    def __init__(self):
        self.ddgs = DDGS()

    def search(self, query, max_results=5):
        """
        General web search
        """

        try:

            results = list(
                self.ddgs.text(
                    query,
                    max_results=max_results
                )
            )

            return results

        except Exception as e:

            return [
                {
                    "title": "Search Error",
                    "body": str(e),
                    "href": ""
                }
            ]

    def news(self, query, max_results=5):
        """
        News search
        """

        try:

            results = list(
                self.ddgs.news(
                    query,
                    max_results=max_results
                )
            )

            return results

        except Exception as e:

            return [
                {
                    "title": "News Error",
                    "body": str(e),
                    "url": ""
                }
            ]