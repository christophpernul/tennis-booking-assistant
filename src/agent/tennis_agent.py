"""
Tennis booking AI agent that processes user requests and suggests available courts.
"""

import re
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

from openai import OpenAI
from agents import Agent, Message

from ..data.courts import COURTS, get_court_by_id, get_courts_by_type
from ..data.user_preferences import user_preferences
from ..booking.stc_client import stc_client, TimeSlot


@dataclass
class BookingRequest:
    """Represents a parsed booking request from the user."""
    user_name: Optional[str] = None
    target_date: Optional[date] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration_hours: Optional[int] = None
    preferred_courts: List[str] = None
    preferred_court_types: List[str] = None
    is_singles: bool = False
    is_doubles: bool = False


@dataclass
class BookingSuggestion:
    """Represents a booking suggestion for the user."""
    court_id: str
    court_name: str
    court_type: str
    location: str
    date: date
    start_time: str
    end_time: str
    duration: str
    is_preferred: bool = False


class TennisBookingAgent:
    """AI agent for tennis court booking assistance."""
    
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)
        self.agent = Agent(
            name="tennis_booking_assistant",
            llm=self.client,
            system_message=self._get_system_message()
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
    
    def process_request(self, user_message: str) -> str:
        """
        Process a user's booking request and return suggestions.
        
        Args:
            user_message: The user's booking request
            
        Returns:
            Formatted response with booking suggestions
        """
        # Parse the user request
        request = self._parse_user_request(user_message)
        
        if not request.target_date:
            return "Bitte gib ein Datum für deine Tennisbuchung an."
        
        # Get available slots
        available_slots = stc_client.get_available_slots(
            request.target_date,
            request.start_time,
            request.end_time
        )
        
        if not available_slots:
            # Try alternative times
            return self._suggest_alternative_times(request)
        
        # Filter and rank suggestions
        suggestions = self._create_booking_suggestions(request, available_slots)
        
        if not suggestions:
            return self._suggest_alternative_times(request)
        
        # Format response
        return self._format_suggestions(suggestions, request)
    
    def _parse_user_request(self, message: str) -> BookingRequest:
        """Parse user message to extract booking details."""
        request = BookingRequest()
        
        # Extract user name (simple pattern matching)
        name_patterns = [
            r"my name is (\w+)",
            r"i'm (\w+)",
            r"i am (\w+)",
            r"this is (\w+)"
        ]
        for pattern in name_patterns:
            match = re.search(pattern, message.lower())
            if match:
                request.user_name = match.group(1).title()
                break
        
        # Extract date
        date_patterns = [
            r"(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})",  # DD/MM/YYYY
            r"(\d{1,2})\.(\d{1,2})\.(\d{2,4})",      # DD.MM.YYYY
            r"today",
            r"tomorrow",
            r"next (\w+)",  # next monday, etc.
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, message.lower())
            if match:
                if pattern == r"today":
                    request.target_date = date.today()
                elif pattern == r"tomorrow":
                    request.target_date = date.today() + timedelta(days=1)
                elif "next" in pattern:
                    # Simple next day logic
                    request.target_date = date.today() + timedelta(days=1)
                else:
                    # Parse specific date
                    day, month, year = match.groups()
                    if len(year) == 2:
                        year = "20" + year
                    request.target_date = date(int(year), int(month), int(day))
                break
        
        # Extract time
        time_patterns = [
            r"(\d{1,2}):(\d{2})",  # HH:MM
            r"(\d{1,2}) (am|pm)",   # 3 pm
            r"(\d{1,2})(am|pm)",    # 3pm
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, message.lower())
            if match:
                hour = int(match.group(1))
                if len(match.groups()) > 1 and match.group(2) == "pm" and hour != 12:
                    hour += 12
                elif match.group(2) == "am" and hour == 12:
                    hour = 0
                request.start_time = f"{hour:02d}:00"
                break
        
        # Extract duration
        duration_patterns = [
            r"(\d+) hour",
            r"(\d+)h",
            r"for (\d+) hour",
        ]
        
        for pattern in duration_patterns:
            match = re.search(pattern, message.lower())
            if match:
                request.duration_hours = int(match.group(1))
                break
        
        # Extract court preferences
        court_keywords = {
            "sand": ["sand", "clay", "red clay", "sandplatz"],
            "granulat": ["granulat", "granule"],
            "wingfield": ["wingfield", "wing field", "wingfield-platz"],
        }
        
        request.preferred_court_types = []
        for court_type, keywords in court_keywords.items():
            if any(keyword in message.lower() for keyword in keywords):
                request.preferred_court_types.append(court_type)
        
        # Extract singles/doubles preference
        if "single" in message.lower() or "einzel" in message.lower():
            request.is_singles = True
        elif "double" in message.lower() or "doppel" in message.lower():
            request.is_doubles = True
        
        return request
    
    def _create_booking_suggestions(self, request: BookingRequest, available_slots: List[TimeSlot]) -> List[BookingSuggestion]:
        """Create booking suggestions based on available slots and user preferences."""
        suggestions = []
        
        # Get user preferences if name is provided
        user_pref_courts = []
        if request.user_name:
            user_pref_courts = user_preferences.get_preferred_courts(request.user_name)
            if not request.preferred_court_types:
                request.preferred_court_types = user_preferences.get_preferred_court_types(request.user_name)
        
        # Group slots by court
        court_slots = {}
        for slot in available_slots:
            if slot.court_id not in court_slots:
                court_slots[slot.court_id] = []
            court_slots[slot.court_id].append(slot)
        
        # Create suggestions
        for court_id, slots in court_slots.items():
            court = get_court_by_id(court_id)
            if not court:
                continue
            
            # Check if court is excluded for this user
            if request.user_name and user_preferences.is_court_excluded(request.user_name, court_id):
                continue  # Skip excluded courts
            
            # Check if court matches preferences
            is_preferred = (
                court_id in user_pref_courts or
                (request.preferred_court_types and court.court_type in request.preferred_court_types)
            )
            
            # Check singles/doubles compatibility
            if request.is_singles and court.is_singles_only:
                # Perfect match for singles
                pass
            elif request.is_doubles and court.is_singles_only:
                # Skip singles-only courts for doubles
                continue
            
            # Create suggestion for each available slot
            for slot in slots:
                suggestion = BookingSuggestion(
                    court_id=court_id,
                    court_name=court.name,
                    court_type=court.court_type,
                    location=court.location,
                    date=request.target_date,
                    start_time=slot.start_time,
                    end_time=slot.end_time,
                    duration="1 hour",
                    is_preferred=is_preferred
                )
                suggestions.append(suggestion)
        
        # Sort by preference and time
        suggestions.sort(key=lambda s: (not s.is_preferred, s.start_time))
        
        return suggestions[:10]  # Limit to top 10 suggestions
    
    def _suggest_alternative_times(self, request: BookingRequest) -> str:
        """Suggest alternative times when requested time is unavailable."""
        # Try next few days
        for days_ahead in [1, 2, 3]:
            alt_date = request.target_date + timedelta(days=days_ahead)
            available_slots = stc_client.get_available_slots(alt_date)
            
            if available_slots:
                suggestions = self._create_booking_suggestions(request, available_slots)
                if suggestions:
                    return f"Keine Verfügbarkeit für {request.target_date.strftime('%d.%m.%Y')}. Hier sind Alternativen für {alt_date.strftime('%d.%m.%Y')}:\n\n" + self._format_suggestions(suggestions[:5], request)
        
        return f"Entschuldigung, keine Plätze verfügbar für {request.target_date.strftime('%d.%m.%Y')} oder die nächsten Tage. Bitte versuche ein anderes Datum."
    
    def _format_suggestions(self, suggestions: List[BookingSuggestion], request: BookingRequest) -> str:
        """Format booking suggestions into a readable response."""
        if not suggestions:
            return "Keine passenden Plätze für deine Anfrage verfügbar."
        
        response = f"🎾 Verfügbare Plätze für {request.target_date.strftime('%d.%m.%Y')}:\n\n"
        
        for i, suggestion in enumerate(suggestions, 1):
            preferred_marker = "⭐ " if suggestion.is_preferred else ""
            response += f"{i}. {preferred_marker}{suggestion.court_name} ({suggestion.court_type})\n"
            response += f"   📍 {suggestion.location}\n"
            response += f"   🕐 {suggestion.start_time} - {suggestion.end_time}\n"
            response += f"   ⏱️ {suggestion.duration}\n\n"
        
        response += "💡 Tipp: Plätze mit ⭐ entsprechen deinen Vorlieben."
        
        return response
