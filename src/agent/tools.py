from agents import function_tool

from src.booking.constants import CourtAvailability
from src.booking.booking_fetcher import CourtBookingFetcher, convert_to_availability


@function_tool
def get_court_availability_tool(date: str) -> list[CourtAvailability]:
    """
    Retrieves court availabilities for `date` for all courts.

    Args:
        date: Date in DD.MM.YYYY format

    Returns:
        List of CourtAvailability objects for all courts on the specified date
    """
    booking_fetcher = CourtBookingFetcher(target_date=date)
    court_availabilities = convert_to_availability(booking_fetcher.get_court_bookings())
    return court_availabilities
