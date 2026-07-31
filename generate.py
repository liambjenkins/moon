import sys
from datetime import date, timedelta

from astronomy import get_moon_data
from models import MoonDay
from calendar import build_calendar, save_calendar


def build_year(year):

    days = []

    current = date(year, 1, 1)
    end = date(year, 12, 31)

    while current <= end:

        data = get_moon_data(current)

        days.append(
            MoonDay(
                date=current,
                phase=data["phase"],
                illumination=data["illumination"],
                sign=data["sign"],
                moonrise=None,
                moonset=None,
                phase_time=None,
                transit_from=None,
                transit_to=None,
                transit_time=None,
            )
        )

        current += timedelta(days=1)

    return days


if __name__ == "__main__":

    year = int(sys.argv[1])

    days = build_year(year)

    calendar = build_calendar(days)

    save_calendar(calendar)

    print(
        f"Moon calendar generated for {year} 🌙"
    )
