from dataclasses import dataclass
from datetime import date


@dataclass
class MoonDay:

    date: date

    phase: str

    illumination: int

    sign: str

    moonrise: object = None

    moonset: object = None

    phase_time: object = None

    transit: object = None

    transit_time: object = None
