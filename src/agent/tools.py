from agents import function_tool

from src.booking.booking_fetcher import CourtBookingFetcher


@function_tool
def get_booking_tool(date: str):
    """Retrieves court bookings for `date` from CourtBookingManager."""
    booking_fetcher = CourtBookingFetcher(target_date=date)
    return booking_fetcher.get_court_bookings()
