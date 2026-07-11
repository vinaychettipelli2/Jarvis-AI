from agents.ai_agent import AIAgent
from agents.memory_agent import MemoryAgent
from agents.research_agent import ResearchAgent
from agents.desktop_agent import DesktopAgent
from agents.voice_agent import VoiceAgent
from agents.trading_agent import TradingAgent
from agents.safety_agent import SafetyAgent
from agents.context_agent import ContextAgent


class AgentManager:

    def __init__(self):

        self.ai = AIAgent()
        self.memory = MemoryAgent()
        self.research = ResearchAgent()
        self.desktop = DesktopAgent()
        self.voice = VoiceAgent()
        self.trading = TradingAgent()
        self.safety = SafetyAgent()
        self.context = ContextAgent()

    # ==========================================================
    # Execute Agent
    # ==========================================================

    def execute(self, agent_name, request):

        # ------------------------------------------------------
        # MEMORY
        # ------------------------------------------------------

        if agent_name == "memory":

            result = self.memory.execute(request)

            if result:

                return result

            return "I couldn't find that information."

        # ------------------------------------------------------
        # RESEARCH
        # ------------------------------------------------------

        elif agent_name == "research":

            return self.research.execute(request)

        # ------------------------------------------------------
        # DESKTOP
        # ------------------------------------------------------

        elif agent_name == "desktop":

            return self.desktop.execute(request)

        # ------------------------------------------------------
        # VOICE
        # ------------------------------------------------------

        elif agent_name == "voice":

            return self.voice.execute(request)

        # ------------------------------------------------------
        # TRADING
        # ------------------------------------------------------

        elif agent_name == "trading":

            return self.trading.execute(request)

        # ------------------------------------------------------
        # SAFETY
        # ------------------------------------------------------

        elif agent_name == "safety":

            return self.safety.execute(request)

        # ------------------------------------------------------
        # AI
        # ------------------------------------------------------

        history = self.context.get_history()

        answer = self.ai.execute(

            request,

            history

        )

        self.context.add(

            "user",

            request

        )

        self.context.add(

            "assistant",

            answer

        )

        return answer   