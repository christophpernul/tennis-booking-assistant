"""
STC (Sport- und Tennis-Club München Süd) booking system client.
Fetches court availability from the eBuSy booking system.
"""

import json
import requests
from collections import defaultdict
from datetime import datetime, date
from typing import Dict, List, Union

from src.booking.constants import COURT_STC_ID_TO_INTERNAL_ID, COURT_INTERNAL_ID_TO_NAME, CourtAvailability, TimeSlot, CourtBookings
from src.utils.validation import validate_date


class STCBookingClient:
    """Client for interacting with the STC eBuSy booking system."""
    
    def __init__(self):
        self.base_url = "https://siemens-tennisclub-muenchenv8.ebusy.de"
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
        })

    def get_court_bookings(self, target_date: Union[date, str]) -> List[CourtAvailability]:
        """
        Fetch court availability for a specific date.
        
        Args:
            target_date: The date to check availability for
            
        Returns:
            List of court availability data
        """
        if isinstance(target_date, date):
            date_str = target_date.strftime("%m/%d/%Y")
        elif isinstance(target_date, str):
            validate_date(date_str=target_date)
            date_str = datetime.strptime(target_date, "%d.%m.%Y").strftime("%m/%d/%Y")
        else:
            raise ValueError("`target_date` must be a date object or a string in format DD.MM.YYYY")
        url = f"{self.base_url}/lite-module/891?timestamp=&currentDate={date_str}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()            
        except requests.RequestException as e:
            print(f"Error fetching availability: {e}")
            return []
        court_bookings = self._parse_court_bookings(data=json.loads(response.content))
        print(f"Fetched bookings for {date_str}: {court_bookings}")
        return court_bookings
    
    def convert_court_id(self, data: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        """
        Converts STC court IDs to internal ID and the resp. court's name.
        """
        court_stc_id_to_name_map = {
            stc_id: COURT_INTERNAL_ID_TO_NAME[internal_id] for stc_id, internal_id in COURT_STC_ID_TO_INTERNAL_ID.items()
        }
        return {
            court_stc_id_to_name_map[stc_id]: bookings for stc_id, bookings in data.items()
        }
    
    def _parse_court_bookings(self, data: Dict[str, List[Dict]]) -> CourtBookings:
        """
        Parse booking data and return a dictionary with STC court IDs as keys
        and lists of booking time slots as values.
        
        Args:
            data (dict): The JSON data containing reservations
            
        Returns:
            dict: Dictionary with STC court IDs as keys and booking lists as values
        """
        # Dictionary to store bookings by court ID
        court_bookings = defaultdict(list)
        
        # Extract reservations from JSON
        reservations = data.get('reservations', [])
        
        # Process each reservation
        for reservation in reservations:
            court_id = reservation.get('court')
            from_time = reservation.get('fromTime')
            to_time = reservation.get('toTime')
            date = datetime.strptime(reservation.get('date'), "%m/%d/%Y").strftime("%d.%m.%Y")
            
            # Add booking to the court's list
            if court_id and from_time and to_time:
                booking = {
                    'fromTime': from_time,
                    'toTime': to_time,
                    'date': date
                }
                court_bookings[court_id].append(booking)
        
        # Convert defaultdict to regular dict and sort bookings by fromTime
        result = {}
        for court_id, bookings in court_bookings.items():
            # Sort bookings by fromTime for better readability
            sorted_bookings = sorted(bookings, key=lambda x: x['fromTime'])
            result[court_id] = sorted_bookings
        return self.convert_court_id(result)
    
    # def get_available_slots(self, target_date: date, start_time: str = None, end_time: str = None) -> List[TimeSlot]:
    #     """
    #     Get available time slots for a specific date and optional time range.
        
    #     Args:
    #         target_date: The date to check
    #         start_time: Optional start time filter (HH:MM format)
    #         end_time: Optional end time filter (HH:MM format)
            
    #     Returns:
    #         List of available time slots
    #     """
    #     courts_availability = self.get_court_availability(target_date)
        
    #     available_slots = []
    #     for court_avail in courts_availability:
    #         for slot in court_avail.time_slots:
    #             if not slot.is_available:
    #                 continue
                
    #             # Apply time filters if provided
    #             if start_time and slot.start_time < start_time:
    #                 continue
    #             if end_time and slot.end_time > end_time:
    #                 continue
                
    #             available_slots.append(slot)
        
    #     return available_slots


# Global instance for easy access
if __name__ == "__main__":
    stc_client = STCBookingClient()
    bookings = stc_client.get_court_bookings(date.today())
    print(bookings)