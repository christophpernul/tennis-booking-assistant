"""
Court data and context information for the tennis booking assistant.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Court:
    """Represents a tennis court with its properties."""
    id: str
    name: str
    location: str  # Location of the court in the club
    is_middle_court: bool  # Whether the court is a middle court
    is_singles_only: bool  # Whether the court is only for singles
    court_type: str  # Type of court (e.g., "clay", "hard", "indoor")
    is_wingfield: bool = False  # Whether the court is a Wingfield court
    is_available: bool = False  # Current availability status


# Court database based on STC eBuSy system
COURTS = [
    Court(
        id="court_a",
        name="Platz A",
        location="Main building, ground floor",
        is_middle_court=False,
        is_singles_only=True,
        court_type="clay"
    ),
    Court(
        id="court_1", 
        name="Platz 1",
        location="Main building, ground floor",
        is_middle_court=False,
        is_singles_only=False,
        court_type="clay"
    ),
    Court(
        id="court_2",
        name="Platz 2", 
        location="Main building, ground floor",
        is_middle_court=True,
        is_singles_only=False,
        court_type="clay"
    ),
    Court(
        id="court_3",
        name="Platz 3",
        location="Main building, ground floor",
        is_middle_court=False,
        is_singles_only=False,
        court_type="clay"
    ),
    Court(
        id="court_4",
        name="Platz 4",
        location="Main building, ground floor",
        is_middle_court=False,
        is_singles_only=False,
        court_type="clay"
    ),
    Court(
        id="court_5",
        name="Platz 5",
        location="Main building, ground floor",
        is_middle_court=False,
        is_singles_only=False,
        court_type="clay"
    ),
    Court(
        id="court_6",
        name="Platz 6",
        location="Main building, ground floor",
        is_middle_court=False,
        is_singles_only=False,
        court_type="clay"
    ),
    Court(
        id="court_7",
        name="Platz 7",
        location="Main building, ground floor",
        is_middle_court=False,
        is_singles_only=False,
        court_type="hard-clay"
    ),
    Court(
        id="court_8",
        name="Platz 8",
        location="Main building, ground floor",
        is_middle_court=False,
        is_singles_only=False,
        court_type="hard-clay"
    ),
    Court(
        id="court_9",
        name="Platz 9",
        location="Main building, ground floor",
        is_middle_court=False,
        is_singles_only=False,
        court_type="hard-clay"
    ),
    Court(
        id="court_10",
        name="Platz 10",
        location="Outdoor area, Granulat courts",
        is_middle_court=False,
        is_singles_only=False,
        court_type="granulat"
    ),
    Court(
        id="court_11",
        name="Platz 11",
        location="Outdoor area, Granulat courts",
        is_middle_court=False,
        is_singles_only=False,
        court_type="granulat"
    ),
    Court(
        id="court_12",
        name="Platz 12",
        location="Outdoor area, Granulat courts",
        is_middle_court=False,
        is_singles_only=False,
        court_type="granulat"
    ),
    Court(
        id="court_t",
        name="T-Platz",
        location="Indoor facility",
        is_middle_court=False,
        is_singles_only=False,
        court_type="clay"
    ),
    Court(
        id="court_14",
        name="Platz 14",
        location="Outdoor area, back courts",
        is_middle_court=False,
        is_singles_only=False,
        court_type="clay"
    ),
    Court(
        id="court_15",
        name="Platz 15",
        location="Outdoor area, back courts",
        is_middle_court=False,
        is_singles_only=False,
        court_type="clay"
    ),
    Court(
        id="court_16",
        name="Platz 16",
        location="Outdoor area, back courts",
        is_middle_court=False,
        is_singles_only=False,
        court_type="clay"
    ),
    Court(
        id="court_17",
        name="Platz 17",
        location="Outdoor area, Wingfield courts",
        is_middle_court=False,
        is_singles_only=False,
        court_type="clay",
        is_wingfield=True
    ),
    Court(
        id="court_18",
        name="Platz 18",
        location="Outdoor area, back courts",
        is_middle_court=False,
        is_singles_only=False,
        court_type="clay"
    ),
    Court(
        id="court_19",
        name="Platz 19",
        location="Outdoor area, back courts",
        is_middle_court=False,
        is_singles_only=False,
        court_type="clay"
    ),
    Court(
        id="court_20",
        name="Platz 20",
        location="Outdoor area, back courts",
        is_middle_court=False,
        is_singles_only=False,
        court_type="clay"
    ),
    Court(
        id="court_21",
        name="Platz 21",
        location="Outdoor area, back courts",
        is_middle_court=False,
        is_singles_only=False,
        court_type="clay"
    ),
    Court(
        id="court_22",
        name="Platz 22",
        location="Outdoor area, back courts",
        is_middle_court=False,
        is_singles_only=False,
        court_type="clay"
    ),
]


def get_court_by_id(court_id: str) -> Optional[Court]:
    """Get a court by its ID."""
    for court in COURTS:
        if court.id == court_id:
            return court
    return None


def get_available_courts() -> List[Court]:
    """Get all available courts."""
    return [court for court in COURTS if court.is_available]


def get_courts_by_type(court_type: str) -> List[Court]:
    """Get courts by type (e.g., 'clay', 'hard', 'indoor')."""
    return [court for court in COURTS if court.court_type.lower() == court_type.lower()]


def get_middle_courts() -> List[Court]:
    """Get all middle courts."""
    return [court for court in COURTS if court.is_middle_court]


def get_singles_courts() -> List[Court]:
    """Get courts that are singles only."""
    return [court for court in COURTS if court.is_singles_only]


def get_wingfield_courts() -> List[Court]:
    """Get courts that are Wingfield courts."""
    return [court for court in COURTS if court.is_wingfield]
