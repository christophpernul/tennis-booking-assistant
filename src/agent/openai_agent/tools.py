from agents import function_tool

from src.data.courts import Court, COURT_ATTRIBUTES
from src.booking.constants import CourtAvailability
from src.booking.booking_fetcher import CourtBookingFetcher


@function_tool
async def get_court_availability_tool(
    # wrapper: RunContextWrapper[BookingContext],
    date: str,
    for_indoors: bool,
) -> list[CourtAvailability]:
    """
    Retrieves court availabilities for `date` for all courts either for indoors only or for outside.

    Args:
        date: Date in DD.MM.YYYY format
        for_indoors: bool, whether to fetch court availability for indoor courts or not

    Returns:
        List of CourtAvailability objects for all courts on the specified date
    """
    booking_fetcher = CourtBookingFetcher(target_date=date, for_indoors=for_indoors)
    court_availabilities = booking_fetcher.get_court_availabilities()

    # wrapper.context.availability = court_availabilities
    return court_availabilities


@function_tool
async def get_court_attributes_tool() -> list[Court]:
    return COURT_ATTRIBUTES


#
#
# @function_tool
# def get_user_preferences_tool(user_name: str) -> dict:
#     """Fetch user preferences from the database or in-memory store."""
#
#     all_preferences = set_user_preferences()
#     return all_preferences.get_user_preferences(user_name)
