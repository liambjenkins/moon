from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class MoonDay:

    date: date

    phase: str

    illumination: int

    sign: str

    lunar_day: int

    phase_time: Optional[datetime] = None

    sign_transition: Optional[dict] = None

    coming: Optional[list] = None
