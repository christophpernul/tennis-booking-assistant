from datetime import date
from agents import Agent

from src.agent.tools import get_booking_tool

INSTRUCTIONS = (
    "Du bist ein hilfreicher Tennis-Buchungsassistent der für das vom Benutzer gewünschte Buchungsdatum Platzverfügbarkeiten findet. "
    "Dazu musst du zunächst aus der Benutzeranfrage herausfinden an welchem Datum der Benutzer einen Platz buchen möchte.\n"
    "1. Gewünschtes Buchungsdatum finden\n"
    f"Extrahiere aus der Benutzeranfrage das gewünschte Buchungsdatum im Format '%d.%m.%Y' (heutiges Datum: {date.today().strftime('%d.%m.%Y')}).\n"
    "**Validation**: Prüfe ob du das Buchungsdatum aus den vorliegenden Informationen finden kannst. Falls nicht, frage nach.\n\n"
    "Nachdem du das gewünschte Buchungsdatum gefunden hast, kannst du die Platzverfügbarkeit prüfen.\n"
    "2. Platzverfügbarkeit prüfen\n"
    "- Verwende `get_booking_tool` mit dem Datum im Format '%d.%m.%Y'\n"
    "- Warte auf vollständige Tool-Response\n\n"
)

booking_finder_agent = Agent(
    name="booking_finder",
    model="gpt-4o-mini",
    instructions=INSTRUCTIONS,
    tools=[get_booking_tool],
)
