"""
Tennis booking AI agent that processes user requests and suggests available courts.
"""

import asyncio
from dataclasses import dataclass
from agents import Agent, trace, Runner, function_tool, gen_trace_id

from src.data.courts import COURT_ATTRIBUTES
from src.data.user_preferences import set_user_preferences
from src.booking.booking_manager import CourtBookingManager

from src.agent.prompts import SYSTEM_PROMPT


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


@function_tool
def get_booking_tool(date: str):
    """Retrieves court bookings for `date` from CourtBookingManager."""
    booking_client = CourtBookingManager(target_date=date)
    return booking_client.get_court_bookings()


@function_tool
def get_court_attributes_tool() -> dict:
    return COURT_ATTRIBUTES


@function_tool
def get_user_preferences_tool(user_name: str) -> dict:
    """Fetch user preferences from the database or in-memory store."""

    all_preferences = set_user_preferences()
    return all_preferences.get_user_preferences(user_name)


class TennisBookingAgent:
    """AI agent for tennis court booking assistance."""

    def __init__(self, openai_api_key: str):
        self.agent = Agent(
            name="tennis_booking_assistant",
            model="gpt-4o-mini",
            instructions=self._get_system_message(),
            tools=[
                get_booking_tool,
                get_court_attributes_tool,
                # get_user_preferences_tool,
            ],
        )

    @staticmethod
    def _get_system_message() -> str:
        """Get the system message for the AI agent."""
        return SYSTEM_PROMPT

    async def _process_request(self, user_message: str) -> str:
        """
        Process a user's booking request and return suggestions.

        Args:
            user_message: The user's booking request

        Returns:
            Response from the AI agent
        """
        # Send the message directly to the agent
        with trace("Tennis Agent", trace_id=gen_trace_id()):
            response = await Runner.run(self.agent, user_message)
        return response.final_output

    def chat_with_agent(
        self, message: str, history: list[dict]
    ) -> tuple[str, list[dict]]:
        """
        Process a chat message and return the agent's response.

        Args:
            message: User's message
            history: Chat history in messages format

        Returns:
            Tuple of (response, updated_history)
        """
        if not message.strip():
            return "", history

        # Process the message with the agent
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            response = loop.run_until_complete(self._process_request(message))
        finally:
            loop.close()

        # Update history with messages format
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})

        return "", history
