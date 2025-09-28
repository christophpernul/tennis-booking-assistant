from datetime import datetime
from pydantic import BaseModel, Field, field_validator

COURT_STC_ID_TO_INTERNAL_ID = {
    1472: 1,
    1473: 2,
    1474: 3,
    1475: 4,
    1476: 5,
    1477: 6,
    1478: 7,
    1479: 8,
    1480: 9,
    1481: 10,
    1482: 11,
    1483: 12,
    1484: 13,
    1485: 14,
    1486: 15,
    1487: 16,
    1488: 17,
    1489: 18,
    1490: 0,
    1491: 19,
    1492: 20,
    1493: 21,
    1494: 22,
}

COURT_INTERNAL_ID_TO_NAME = {
    0: "Platz A",
    1: "Platz 1",
    2: "Platz 2",
    3: "Platz 3",
    4: "Platz 4",
    5: "Platz 5",
    6: "Platz 6",
    7: "Platz 7",
    8: "Platz 8",
    9: "Platz 9",
    10: "Platz 10",
    11: "Platz 11",
    12: "Platz 12",
    13: "Platz T",
    14: "Platz 14",
    15: "Platz 15",
    16: "Platz 16",
    17: "Platz 17",
    18: "Platz 18",
    19: "Platz 19",
    20: "Platz 20",
    21: "Platz 21",
    22: "Platz 22",
}

COURT_NAME_TO_INTERNAL_ID: dict = {
    name: id for id, name in COURT_INTERNAL_ID_TO_NAME.items()
}


class CourtBooking(BaseModel):
    """Represents a single booking / reservation of a court."""

    court_name: str = Field(description="The name of the court being booked")
    start_time: datetime = Field(description="The start date and time of the booking")
    end_time: datetime = Field(description="The end date and time of the booking")

    @field_validator("end_time")
    @classmethod
    def validate_end_time_after_start(cls, v, info):
        if "start_time" in info.data and v <= info.data["start_time"]:
            raise ValueError("End time must be after start time")
        return v


class CourtAvailability(BaseModel):
    """Represents a full day schedule for a single court"""

    court_name: str = Field(..., description="Name of the court")
    availability: dict[int, bool] = Field(description="Hour to availability mapping")

    def is_available(self, hour: int) -> bool:
        return self.availability.get(hour, False)

    def set_availability(self, hour: int, available: bool):
        self.availability[hour] = available
