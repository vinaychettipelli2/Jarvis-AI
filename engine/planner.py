from core.intent_detector import IntentDetector


class Planner:

    def __init__(self):

        self.intent = IntentDetector()

    def plan(self, question):

        """
        Decide which agent should execute the request.
        """

        return self.intent.detect(question)