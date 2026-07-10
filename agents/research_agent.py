from services.research_service import ResearchService


class ResearchAgent:
    """
    Research Agent

    Responsibilities:
    - Internet Search
    - Latest News
    - Weather
    - Cryptocurrency
    - AI Summaries
    """

    def __init__(self):

        self.research_service = ResearchService()

    # =====================================================
    # Main Entry Point
    # =====================================================

    def execute(self, request):

        result = self.research_service.summarize(request)

        if not result.get("success"):

            return (
                result.get(
                    "message",
                    "Unable to complete research."
                )
            )

        return result["message"]    