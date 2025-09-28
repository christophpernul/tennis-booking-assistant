from agents import function_tool, RunContextWrapper

from src.booking.constants import CourtAvailability
from src.booking.booking_fetcher import CourtBookingFetcher, convert_to_availability
from src.agent.prompts import BookingContext


@function_tool
def get_court_availability_tool(
    # wrapper: RunContextWrapper[BookingContext],
    date: str,
) -> list[CourtAvailability]:
    """
    Retrieves court availabilities for `date` for all courts.

    Args:
        date: Date in DD.MM.YYYY format

    Returns:
        List of CourtAvailability objects for all courts on the specified date
    """
    booking_fetcher = CourtBookingFetcher(target_date=date)
    court_availabilities = convert_to_availability(booking_fetcher.get_court_bookings())

    # wrapper.context.availability = court_availabilities
    return court_availabilities


# @function_tool
# def get_court_attributes_tool() -> dict:
#     return COURT_ATTRIBUTES
#
#
# @function_tool
# def get_user_preferences_tool(user_name: str) -> dict:
#     """Fetch user preferences from the database or in-memory store."""
#
#     all_preferences = set_user_preferences()
#     return all_preferences.get_user_preferences(user_name)
