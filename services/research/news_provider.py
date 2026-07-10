from duckduckgo_search import DDGS


class NewsProvider:

    """
    News Provider

    Retrieves the latest news articles.
    """

    def __init__(self):

        self.ddgs = DDGS()

    def search(self, topic, max_results=5):

        try:

            results = list(

                self.ddgs.news(

                    topic,

                    max_results=max_results

                )

            )

            return {

                "success": True,

                "results": results

            }

        except Exception as e:

            return {

                "success": False,

                "message": str(e),

                "results": []

            }