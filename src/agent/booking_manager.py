"""
Tennis booking AI agent that processes user requests and suggests available courts.
"""

from agents import Agent, trace, Runner, SQLiteSession, gen_trace_id

from src.agent.prompts import SYSTEM_PROMPT
from src.agent.tools import get_court_availability_tool

# from src.agent.prompts import BookingContext


class BookingManager:
    """AI agent for tennis court booking assistance."""

    # TODO: Now the agent does not know the fetched availabilities as context and only knows after using the tool
    # and forgets this data later. We should add the data to the context of the agent.

    def __init__(self, openai_api_key: str):
        # self.context = BookingContext(availability=[])
        # self.agent = Agent[BookingContext](
        self.agent = Agent(
            name="BookingRecommender",
            model="gpt-4o-mini",
            instructions=self._get_system_message(),
            tools=[get_court_availability_tool],
        )
        self.trace_id = gen_trace_id()
        self.session = SQLiteSession(self.trace_id)

    @staticmethod
    def _get_system_message() -> str:
        """Get the system message for the AI agent."""
        return SYSTEM_PROMPT

    async def _run_manager(self, user_message: str) -> str:
        """Run the agent with the given user message."""
        print("Starting booking manager...")
        response = await Runner.run(
            self.agent,
            user_message,
            session=self.session,  # context=self.context
        )
        return response.final_output

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
                response = await self._run_manager(message)
        except Exception as e:
            print(f"Error processing request: {e}")
            response = "I'm sorry, I encountered an error processing your request. Please try again."

        # Update history with messages format
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})

        return "", history
