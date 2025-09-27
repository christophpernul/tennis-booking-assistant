"""
Tennis booking AI agent that processes user requests and suggests available courts.
"""

from dataclasses import dataclass
from agents import Agent, trace, Runner, function_tool, gen_trace_id

from src.data.courts import COURT_ATTRIBUTES
from src.data.user_preferences import set_user_preferences

from src.booking.constants import CourtBooking
from src.booking.booking_fetcher import CourtBookingFetcher

from src.agent.prompts import SYSTEM_PROMPT
from src.agent.booking_finder import booking_finder_agent
from src.agent.booking_recommender import booking_recommender_agent


@dataclass
class BookingSuggestion:
    """Represents a booking suggestion for the user."""

    court_id: str
    court_name: str
    court_type: str
    location: str
    date: str
    start_time: str
    end_time: str
    duration: str
    is_preferred: bool = False


# @function_tool
# def get_booking_tool(date: str):
#     """Retrieves court bookings for `date` from CourtBookingManager."""
#     booking_fetcher = CourtBookingFetcher(target_date=date)
#     return booking_fetcher.get_court_bookings()
#
#
# @function_tool
# def get_court_attributes_tool() -> dict:
#     return COURT_ATTRIBUTES
#
#
# @function_tool
# def get_user_preferences_tool(user_name: str) -> dict:
#     """Fetch user preferences from the database or in-memory store."""
#
#     all_preferences = set_user_preferences()
#     return all_preferences.get_user_preferences(user_name)


class BookingManager:
    """AI agent for tennis court booking assistance."""

    def __init__(self, openai_api_key: str):
        self.agent = Agent(
            name="manager",
            model="gpt-4o-mini",
            instructions=self._get_system_message(),
            # tools=[],
            handoffs=[booking_finder_agent, booking_recommender_agent],
        )

    #   File "D:\Documents\Projects\tennis-booking-assistant\.venv\Lib\site-packages\gradio\components\chatbot.py", line 574, in _postprocess_content
    #     raise ValueError(f"Invalid message for Chatbot component: {chat_message}")
    # ValueError: Invalid message for Chatbot component: bookings=[Court
    # TODO: The handoff means the sub agent will respond with some text, but the output is the booking list.
    @staticmethod
    def _get_system_message() -> str:
        """Get the system message for the AI agent."""
        return SYSTEM_PROMPT

    async def _run_manager(self, user_message: str) -> str:
        """Run the agent with the given user message."""
        print("Starting booking manager...")
        response = await Runner.run(self.agent, user_message)
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

        trace_id = gen_trace_id()
        try:
            with trace("Tennis Agent", trace_id=trace_id):
                print(
                    f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
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
