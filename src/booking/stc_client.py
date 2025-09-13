"""
STC (Sport- und Tennis-Club München Süd) booking system client.
Fetches court availability from the eBuSy booking system.
"""

import json
import requests
from datetime import datetime, date

from src.booking.constants import (
    COURT_STC_ID_TO_INTERNAL_ID,
    COURT_INTERNAL_ID_TO_NAME,
    CourtBooking,
)
from src.utils.validation import validate_date


class CourtBookingManager:
    """Manages all court bookings on a given date via the STC eBuSy booking system."""

    def __init__(self, target_date: date | str):
        self.target_date = self._parse_target_date(target_date)

        raw_bookings = self._fetch_all_bookings()
        self.court_bookings = self._parse_court_bookings(raw_bookings)

    @staticmethod
    def _parse_target_date(target_date: date | str) -> str:
        """Validate and parse the target date to the expected format '%m/%d/%Y'."""
        if isinstance(target_date, date):
            date_str = target_date.strftime("%m/%d/%Y")
        elif isinstance(target_date, str):
            validate_date(date_str=target_date)
            date_str = datetime.strptime(target_date, "%d.%m.%Y").strftime("%m/%d/%Y")
        else:
            raise ValueError(
                "`target_date` must be a date object or a string in format DD.MM.YYYY"
            )
        return date_str

    def _fetch_all_bookings(self) -> dict:
        """
        Fetch court bookings for a specific target date.

        Returns:
            Raw JSON data from the booking system
        """
        base_url = "https://siemens-tennisclub-muenchenv8.ebusy.de"
        url = f"{base_url}/lite-module/891?timestamp=&currentDate={self.target_date}"

        session = requests.Session()
        session.headers.update(
            {
                "Accept": "application/json",
            }
        )
        try:
            response = session.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching availability: {e}")
            return {}
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return {}
        return data

    def _parse_court_bookings(self, data: dict[str, list[dict]]) -> list[CourtBooking]:
        """
        Parse booking data and return a dictionary with STC court IDs as keys
        and lists of booking time slots as values.

        Args:
            data (dict): The JSON data containing reservations

        Returns:
            list[CourtBooking]: List of court bookings
        """
        court_bookings = []

        reservations = data.get("reservations", [])
        for reservation in reservations:
            booking = self._parse_reservation_booking(reservation)
            court_bookings.append(booking)
        return court_bookings

    @staticmethod
    def _convert_court_stc_id_to_name(stc_id: int) -> str:
        """
        Converts STC court IDs to internal ID and the resp. court's name.
        """
        court_stc_id_to_name_map = {
            stc_id: COURT_INTERNAL_ID_TO_NAME[internal_id]
            for stc_id, internal_id in COURT_STC_ID_TO_INTERNAL_ID.items()
        }
        return court_stc_id_to_name_map[stc_id]

    def _parse_reservation_booking(self, reservation: dict) -> CourtBooking | None:
        """From a reservation entry, parse and return a CourtBooking object."""
        court_id = reservation.get("court")
        if not court_id:
            raise ValueError(
                f"Missing court ID in reservation data: {repr(reservation)}"
            )

        reservation_date = datetime.strptime(reservation.get("date"), "%m/%d/%Y").date()
        if not reservation_date:
            raise ValueError(f"Missing date in reservation data: {repr(reservation)}")
        try:
            from_time = datetime.strptime(reservation.get("fromTime"), "%H:%M").time()
            start_time = datetime.combine(reservation_date, from_time)
        except (ValueError, TypeError):
            raise ValueError(
                f"Invalid date format in reservation data! Got '{reservation.get('fromTime')}'"
            )
        try:
            to_time = datetime.strptime(reservation.get("toTime"), "%H:%M").time()
            end_time = datetime.combine(reservation_date, to_time)
        except (ValueError, TypeError):
            raise ValueError(
                f"Invalid date format in reservation data! Got '{reservation.get('toTime')}'"
            )
        return CourtBooking(
            court_name=self._convert_court_stc_id_to_name(court_id),
            start_time=start_time,
            end_time=end_time,
        )

    def get_court_bookings(self) -> list[CourtBooking]:
        return self.court_bookings.copy()

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
    stc_client = CourtBookingManager(date.today())
    bookings = stc_client.get_court_bookings()
    print(bookings)
