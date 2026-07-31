from dataclasses import dataclass
from datetime import date, time


@dataclass
class MoonDay:
    date: date

    phase: str
    illumination: int
    sign: str

    moonrise: time | None
    moonset: time | None

    phase_time: time | None

    transit_from: str | None
    transit_to: str | None
    transit_time: time | None
