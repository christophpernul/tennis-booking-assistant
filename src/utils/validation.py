import os
from datetime import datetime

from src.constants import (
    ENV_VAR_NAME_SERVER_NAME,
    ENV_VAR_NAME_SERVER_PORT,
    ENV_VAR_NAME_OPENAI_API_KEY,
)


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
        raise ValueError(
            f"Invalid date format. Please use {expected_format}. Got: {date_str}"
        )


def check_requirements():
    """Check if required environment variables are set."""
    required_vars = [
        ENV_VAR_NAME_SERVER_NAME,
        ENV_VAR_NAME_SERVER_PORT,
        ENV_VAR_NAME_OPENAI_API_KEY,
    ]
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease create a .env file in the project root with:")
        for var in missing_vars:
            print(f"   {var}=your_value_here")
        return False

    return True
