from agents import function_tool

from src.booking.booking_fetcher import CourtBookingFetcher, convert_to_availability


@function_tool
def get_court_availability_tool(date: str):
    """Retrieves court availabilities for `date` from CourtBookingManager."""
    booking_fetcher = CourtBookingFetcher(target_date=date)
    court_availabilities = convert_to_availability(booking_fetcher.get_court_bookings())
    return court_availabilities
