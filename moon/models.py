from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class MoonDay:
    """
    Represents lunar information for a single calendar day.
    """

    date: date

    phase: str

    illumination: int

    sign: str

    moonrise: Optional[datetime] = None

    moonset: Optional[datetime] = None

    phase_time: Optional[datetime] = None

    transit: Optional[datetime] = None

    transit_time: Optional[datetime] = None
