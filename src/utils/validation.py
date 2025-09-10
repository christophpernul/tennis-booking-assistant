from datetime import datetime


def validate_date(date_str: str, expected_format: str = "%d.%m.%Y") -> None:
    """
    Validate if the given string is a valid date in format %d.%m.%Y.

    Args:
        date_str (str): The date string to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, expected_format)
    except ValueError:
        raise ValueError(f"Invalid date format. Please use {expected_format}. Got: {date_str}")
