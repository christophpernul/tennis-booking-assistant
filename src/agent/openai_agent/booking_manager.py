"""
Tennis booking AI agent that suggests available courts.
"""

from agents import Agent, Runner, SQLiteSession

from src.agent.openai_agent.prompts import SYSTEM_PROMPT
from src.agent.openai_agent.tools import get_court_availability_tool


class OpenAIAgent:
    def __init__(self, trace_id: str, openai_api_key: str, openai_model: str):
        # self.context = BookingContext(availability=[])
        # self.agent = Agent[BookingContext](
        self.agent = Agent(
            name="BookingRecommender",
            model=openai_model,
            instructions=self._get_system_message(),
            tools=[get_court_availability_tool],
        )
        self.session = SQLiteSession(trace_id)
        # TODO: Now the agent does not know the fetched availabilities as context and only knows after using the tool
        # and forgets this data later. We should add the data to the context of the agent.

    @staticmethod
    def _get_system_message() -> str:
        """Get the system message for the AI agent."""
        return SYSTEM_PROMPT

    async def run_agent(self, user_message: str) -> str:
        """Run the agent with the given user message."""
        print("Starting booking manager...")
        response = await Runner.run(
            self.agent,
            user_message,
            session=self.session,
            # context=self.context
        )
        return response.final_output
