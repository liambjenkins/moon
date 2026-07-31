from dataclasses import dataclass
from datetime import date, time


@dataclass
class MoonDay:
    date: date

    phase: str
    illumination: int
    sign: str

    phase_time: time | None = None

    moonrise: time | None = None
    moonset: time | None = None

    transit_from: str | None = None
    transit_to: str | None = None
    transit_time: time | None = None
