from dataclasses import dataclass


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
