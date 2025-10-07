"""
Tennis booking AI agent that processes user requests and suggests available courts.
"""

from agents import Agent, Runner, SQLiteSession, trace, gen_trace_id

from src.agent.openai_agent.prompts import SYSTEM_PROMPT
from src.agent.openai_agent.tools import (
    get_court_availability_tool,
    get_court_attributes_tool,
)


class OpenAIAgent:
    def __init__(self, trace_id: str, openai_api_key: str, openai_model: str):
        # self.context = BookingContext(availability=[])
        # self.agent = Agent[BookingContext](
        self.agent = Agent(
            name="BookingRecommender",
            model=openai_model,
            instructions=self._get_system_message(),
            tools=[
                get_court_availability_tool,
                get_court_attributes_tool,
            ],
        )
        self.session = SQLiteSession(trace_id)

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


class BookingManager:
    """AI agent for tennis court booking assistance."""

    def __init__(self, openai_api_key: str, openai_model: str):
        self.trace_id = gen_trace_id()
        self.openai_agent = OpenAIAgent(
            trace_id=self.trace_id,
            openai_api_key=openai_api_key,
            openai_model=openai_model,
        )

    async def run(
        self, message: str, history: list[dict] = None
    ) -> tuple[str, list[dict]]:
        """
        Process a chat message and return the agent's response.

        Args:
            message: User's message
            history: Chat history in messages format

        Returns:
            Tuple of (response, updated_history)
        """
        if history is None:
            history = []

        if not message.strip():
            return "", history

        try:
            with trace("Tennis Agent", trace_id=self.trace_id):
                print(
                    f"View trace: https://platform.openai.com/traces/trace?trace_id={self.trace_id}"
                )
                # yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
                response = await self.openai_agent.run_agent(message)
        except Exception as e:
            print(f"Error processing request: {e}")
            response = "I'm sorry, I encountered an error processing your request. Please try again."

        # Update history with messages format
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})

        return response, history
