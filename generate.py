from datetime import date, timedelta
import sys

from moon.astronomy import get_raw_moon_data
from moon.models import MoonDay
from moon.phases import get_phase, get_illumination
from moon.phase_events import find_phase_event
from moon.rise_set import get_rise_set
from moon.feed import build_feed, save_feed
from moon.formatter import format_title, format_notes


def get_sign(longitude):

    signs = [
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces",
    ]

    return signs[int(longitude // 30)]


def build_day(current):

    raw = get_raw_moon_data(current)

    angle = raw["angle"]

    rise_set = get_rise_set(current)

    phase_event = find_phase_event(current)

    return MoonDay(
        date=current,
        phase=get_phase(angle),
        illumination=get_illumination(angle),
        sign=get_sign(raw["longitude"]),
        phase_time=(
            phase_event["time"].time()
            if phase_event
            and phase_event["phase"] == get_phase(angle)
            else None
        ),
        moonrise=rise_set["moonrise"],
        moonset=rise_set["moonset"],
    )


def build_days(year):

    current = date(year, 1, 1)

    end = date(year + 1, 1, 1)

    days = []

    while current < end:

        days.append(
            build_day(current)
        )

        current += timedelta(days=1)

    return days


def build_events(days):

    from icalendar import Event

    events = []

    for day in days:

        event = Event()

        event.add(
            "summary",
            format_title(day)
        )

        event.add(
            "dtstart",
            day.date
        )

        event.add(
            "description",
            format_notes(day)
        )

        event.add(
            "uid",
            f"moon-{day.date}"
        )

        events.append(event)

    return events


if __name__ == "__main__":

    year = int(
        sys.argv[1]
    )

    days = build_days(year)

    events = build_events(days)

    calendar = build_feed(events)

    save_feed(calendar)

    print(
        f"Moon calendar generated for {year} 🌙"
    )
