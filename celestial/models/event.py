from dataclasses import dataclass
from datetime import datetime


@dataclass
class CelestialEvent:
    name: str
    datetime: datetime
    category: str
    importance: float
    description: str