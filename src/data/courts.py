"""
Court data and context information for the tennis booking assistant.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


from pydantic import BaseModel, Field


class Court(BaseModel):
    """Represents a tennis court with its properties."""

    id: int = Field(description="Unique identifier for the court")
    name: str = Field(
        description="Display name of the court (e.g., 'Platz 1', 'Platz A')"
    )
    location: str = Field(
        description="Physical location of the court within the club grounds"
    )
    is_middle_court: bool = Field(
        description="True if court is positioned in the middle (affects accessibility/desirability)",
    )
    is_singles_only: bool = Field(
        description="True if court dimensions/markings are singles-only (not suitable for doubles)",
    )
    court_type: str = Field(description="Surface material: 'sand' or 'granulat'")
    is_wingfield: bool = Field(
        default=False,
        description="True if court has a Wingfield system installed",
    )
    is_indoors: bool = Field(
        default=False,
        description="True if court has roof/enclosure for winter play. IIf true, only true if between end of September and end of April.",
    )


# Court database based on STC eBuSy system
COURT_ATTRIBUTES = [
    Court(
        id=0,
        name="Platz A",
        location="links, Aufschlagtrainingsplatz, Ballmaschinenplatz",
        is_middle_court=False,
        is_singles_only=True,
        is_indoors=False,
        court_type="sand",
    ),
    Court(
        id=1,
        name="Platz 1",
        location="links",
        is_middle_court=True,
        is_singles_only=False,
        is_indoors=False,
        court_type="sand",
    ),
    Court(
        id=2,
        name="Platz 2",
        location="links, Tennisschule",
        is_middle_court=True,
        is_singles_only=False,
        is_indoors=False,
        court_type="sand",
    ),
    Court(
        id=3,
        name="Platz 3",
        location="links, Tennisschule",
        is_middle_court=True,
        is_singles_only=False,
        is_indoors=False,
        court_type="sand",
    ),
    Court(
        id=4,
        name="Platz 4",
        location="links, Tennisschule",
        is_middle_court=True,
        is_singles_only=False,
        is_indoors=False,
        court_type="sand",
    ),
    Court(
        id=5,
        name="Platz 5",
        location="links, Tennisschule",
        is_middle_court=True,
        is_singles_only=False,
        is_indoors=False,
        court_type="sand",
    ),
    Court(
        id=6,
        name="Platz 6",
        location="links, Tennisschule",
        is_middle_court=False,
        is_singles_only=False,
        is_indoors=False,
        court_type="sand",
    ),
    Court(
        id=7,
        name="Platz 7",
        location="Eingang rechts, Sandplätze",
        is_middle_court=False,
        is_singles_only=False,
        is_indoors=True,
        court_type="sand",
    ),
    Court(
        id=8,
        name="Platz 8",
        location="Eingang rechts, Sandplätze",
        is_middle_court=True,
        is_singles_only=False,
        is_indoors=True,
        court_type="sand",
    ),
    Court(
        id=9,
        name="Platz 9",
        location="Eingang rechts, Sandplätze",
        is_middle_court=False,
        is_singles_only=False,
        is_indoors=True,
        court_type="sand",
    ),
    Court(
        id=10,
        name="Platz 10",
        location="Eingang rechts, Granulatplätze",
        is_middle_court=False,
        is_singles_only=False,
        is_indoors=True,
        court_type="granulat",
    ),
    Court(
        id=11,
        name="Platz 11",
        location="Eingang rechts, Granulatplätze",
        is_middle_court=True,
        is_singles_only=False,
        is_indoors=True,
        court_type="granulat",
    ),
    Court(
        id=12,
        name="Platz 12",
        location="Eingang rechts, Granulatplätze",
        is_middle_court=False,
        is_singles_only=False,
        is_indoors=True,
        court_type="granulat",
    ),
    Court(
        id=13,
        name="Platz T",
        location="Mitte, vor dem Restaurant",
        is_middle_court=False,
        is_singles_only=True,
        is_indoors=False,
        court_type="sand",
    ),
    Court(
        id=14,
        name="Platz 14",
        location="hinten rechts, beim Park",
        is_middle_court=False,
        is_singles_only=False,
        is_indoors=False,
        court_type="sand",
    ),
    Court(
        id=15,
        name="Platz 15",
        location="hinten rechts",
        is_middle_court=True,
        is_singles_only=False,
        is_indoors=False,
        court_type="sand",
    ),
    Court(
        id=16,
        name="Platz 16",
        location="hinten rechts",
        is_middle_court=False,
        is_singles_only=False,
        court_type="sand",
    ),
    Court(
        id=17,
        name="Platz 17",
        location="hinten Mitte, Wingfield",
        is_middle_court=False,
        is_singles_only=False,
        is_indoors=False,
        court_type="sand",
        is_wingfield=True,
    ),
    Court(
        id=18,
        name="Platz 18",
        location="hinten Mitte",
        is_middle_court=True,
        is_singles_only=False,
        is_indoors=False,
        court_type="sand",
    ),
    Court(
        id=19,
        name="Platz 19",
        location="hinten Mitte",
        is_middle_court=False,
        is_singles_only=False,
        is_indoors=False,
        court_type="sand",
    ),
    Court(
        id=20,
        name="Platz 20",
        location="hinten links",
        is_middle_court=False,
        is_singles_only=False,
        is_indoors=False,
        court_type="sand",
    ),
    Court(
        id=21,
        name="Platz 21",
        location="hinten links",
        is_middle_court=True,
        is_singles_only=False,
        is_indoors=False,
        court_type="sand",
    ),
    Court(
        id=22,
        name="Platz 22",
        location="hinten links",
        is_middle_court=False,
        is_singles_only=False,
        is_indoors=False,
        court_type="sand",
    ),
]


def get_court_names() -> list[str]:
    """Get a list of all court names."""
    return [court.name for court in COURT_ATTRIBUTES]


def get_court_by_id(court_id: int) -> Optional[Court]:
    """Get a court by its ID."""
    for court in COURT_ATTRIBUTES:
        if court.id == court_id:
            return court
    return None


def get_available_courts() -> List[Court]:
    """Get all available courts."""
    return [court for court in COURT_ATTRIBUTES if court.is_available]


def get_courts_by_type(court_type: str) -> List[Court]:
    """Get courts by type (e.g., 'clay', 'hard', 'indoor')."""
    return [
        court
        for court in COURT_ATTRIBUTES
        if court.court_type.lower() == court_type.lower()
    ]


def get_middle_courts() -> List[Court]:
    """Get all middle courts."""
    return [court for court in COURT_ATTRIBUTES if court.is_middle_court]


def get_singles_courts() -> List[Court]:
    """Get courts that are singles only."""
    return [court for court in COURT_ATTRIBUTES if court.is_singles_only]


def get_wingfield_courts() -> List[Court]:
    """Get courts that are Wingfield courts."""
    return [court for court in COURT_ATTRIBUTES if court.is_wingfield]
