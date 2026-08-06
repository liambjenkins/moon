from dataclasses import dataclass
from datetime import datetime


@dataclass
class BirthData:
    datetime: datetime
    latitude: float
    longitude: float
    timezone: str