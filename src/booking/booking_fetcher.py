"""
STC (Sport- und Tennis-Club München Süd) booking system client.
Fetches court availability from the eBuSy booking system.
"""

import json
import requests
from datetime import datetime, date, timedelta

from src.booking.constants import (
    COURT_STC_ID_TO_INTERNAL_ID,
    COURT_INTERNAL_ID_TO_NAME,
    CourtBooking,
    CourtAvailability,
)
from src.utils.validation import validate_date
from src.data.courts import get_court_names


class CourtBookingFetcher:
    """Fetches all court bookings on a given date via the STC eBuSy booking system."""

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
        booking_dict = {}

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
        booking_dict["court_name"] = self._convert_court_stc_id_to_name(court_id)
        booking_dict["start_time"] = start_time
        booking_dict["end_time"] = end_time

        return CourtBooking(**booking_dict)

    def get_court_bookings(self) -> list[CourtBooking]:
        return self.court_bookings.copy()


def convert_to_availability(bookings: list[CourtBooking]) -> list[CourtAvailability]:
    """
    Convert court bookings to availability structure.

    Args:
        bookings: List of CourtBooking objects

    Returns:
        Dictionary with court names as keys and hour->availability mapping as values
        True means available, False means booked
    """
    all_court_availabilities = []

    all_court_names = set(get_court_names())
    for court_name in sorted(all_court_names):
        print(f"Processing court: {court_name}")
        bookable_hours = {hour: True for hour in range(7, 22)}
        court_bookings = [b for b in bookings if b.court_name == court_name]
        for booking in court_bookings:
            print(f"  Booking from {booking.start_time} to {booking.end_time}")
            current_time = booking.start_time
            while current_time < booking.end_time:
                current_hour = current_time.hour

                hour_start = current_time
                hour_end = current_time + timedelta(hours=1)
                if not (
                    booking.end_time <= hour_start or booking.start_time >= hour_end
                ):
                    print(f"    Marking hour {current_hour} as booked")
                    bookable_hours[current_hour] = False

                current_time += timedelta(hours=1)
        court_availability = CourtAvailability(
            court_name=court_name, availability=bookable_hours
        )
        all_court_availabilities.append(court_availability)

    return all_court_availabilities


# Global instance for easy access
if __name__ == "__main__":
    stc_client = CourtBookingFetcher(date.today())
    bookings = stc_client.get_court_bookings()
    avails = convert_to_availability(bookings)
    print(bookings)
    print(avails)
