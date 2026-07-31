from dataclasses import dataclass
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class Location:

    name: str

    latitude: float

    longitude: float

    timezone: str



MELBOURNE = Location(
    name="Melbourne, Australia",
    latitude=-37.8136,
    longitude=144.9631,
    timezone="Australia/Melbourne",
)


MELBOURNE_TZ = ZoneInfo(
    MELBOURNE.timezone
)


START_DATE = "2026-01-01"

YEARS_FORWARD = 5
