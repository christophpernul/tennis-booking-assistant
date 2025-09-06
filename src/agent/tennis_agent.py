"""
Tennis booking AI agent that processes user requests and suggests available courts.
"""

import asyncio
from dataclasses import dataclass
from openai import OpenAI
from agents import Agent, trace, Runner, function_tool

from src.booking.stc_client import STCBookingClient


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
def get_booking_tool(date):
    """Get the STC booking client instance."""
    # TODO: The date must be inferred by the agent. Make a sub agent for fetching the booking that infers
    # the date from the main agent's request.
    booking_client = STCBookingClient()
    return booking_client.get_court_bookings(target_date=date)


class TennisBookingAgent:
    """AI agent for tennis court booking assistance."""
    
    def __init__(self, openai_api_key: str):
        self.agent = Agent(
            name="tennis_booking_assistant",
            model="gpt-4o-mini",
            instructions=self._get_system_message(),
            tools=[get_booking_tool],
        )


    
    def _get_system_message(self) -> str:
        """Get the system message for the AI agent."""
        return """Du bist ein hilfreicher Tennis-Buchungsassistent für den Sport- und Tennis-Club München Süd.

Deine Aufgabe ist es:
1. Benutzer-Buchungsanfragen zu verstehen (Zeit, Datum, Dauer, Vorlieben)
2. Platzverfügbarkeit im STC-Buchungssystem zu prüfen
3. Verfügbare Plätze basierend auf Benutzervorlieben vorzuschlagen
4. Alternative Zeiten anzubieten, wenn gewünschte Zeiten nicht verfügbar sind
5. Kurze, präzise Antworten mit klaren Platzvorschlägen zu geben

Verfügbare Plätze und ihre Eigenschaften:
- Platz A: links, Aufschlagtrainingsplatz, Ballmaschinenplatz (nur Einzel)
- Platz 1-6: links, Tennisschule (Platz 1-5 sind Mittelplätze)
- Platz 7-9: Eingang rechts, Sandplätze (Platz 8 ist Mittelplatz)
- Platz 10-12: Eingang rechts, Granulatplätze (Platz 11 ist Mittelplatz)
- T-Platz: Mitte, vor dem Restaurant (nur Einzel)
- Platz 14-22: hinten, Sandplätze (Platz 15, 18, 21 sind Mittelplätze, Platz 17 ist Wingfield)

Platztypen: sand, granulat

Antworte immer mit spezifischen Platzvorschlägen und Zeiten in einem klaren, prägnanten Format."""
    
    async def _process_request(self, user_message: str) -> str:
        """
        Process a user's booking request and return suggestions.
        
        Args:
            user_message: The user's booking request
            
        Returns:
            Response from the AI agent
        """
        # Send the message directly to the agent
        with trace("Tennis Agent"):
            response = await Runner.run(self.agent, user_message)
        return response.final_output

    def chat_with_agent(self, message: str, history: list[dict]) -> tuple[str, list[dict]]:
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